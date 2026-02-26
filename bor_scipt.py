import os
import time
import feedparser
import requests
from telegram import Bot

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]
RSS_URL = os.environ["RSS_URL"]

bot = Bot(token=TOKEN)

def get_posted_links():
    if os.path.exists("posted.txt"):
        with open("posted.txt", "r") as f:
            return set(f.read().splitlines())
    return set()

def save_posted_link(link):
    with open("posted.txt", "a") as f:
        f.write(link + "\n")

posted = get_posted_links()

while True:
    try:
        feed = feedparser.parse(RSS_URL)

        for entry in reversed(feed.entries[:5]):
            if entry.link not in posted:
                text = f"{entry.title}"

                # Проверяем наличие фото
                media = entry.get("media_content", [])

                if media:
                    photo_url = media[0]["url"]
                    bot.send_photo(chat_id=CHANNEL_ID, photo=photo_url, caption=text)
                else:
                    bot.send_message(chat_id=CHANNEL_ID, text=text)

                save_posted_link(entry.link)
                posted.add(entry.link)

        time.sleep(600)

    except Exception as e:
        print("Error:", e)
        time.sleep(60)