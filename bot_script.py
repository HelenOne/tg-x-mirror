import os
import feedparser
from telegram import Bot

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]
RSS_URL = os.environ["RSS_URL"]

bot = Bot(token=TOKEN)

def main():
    feed = feedparser.parse(RSS_URL)

    if not feed.entries:
        print("No entries found")
        return

    entry = feed.entries[0]
    text = entry.title
    media = entry.media_content if hasattr(entry, "media_content") else []

    if media:
        photo_url = media[0]["url"]
        bot.send_photo(chat_id=CHANNEL_ID, photo=photo_url, caption=text)
    else:
        bot.send_message(chat_id=CHANNEL_ID, text=text)

    print("Posted latest tweet successfully")

if __name__ == "__main__":
    main()