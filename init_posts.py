import os
import time
import re
import feedparser
from telegram import Bot
from telegram import InputMediaPhoto

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]
RSS_URL = os.environ["RSS_URL"]

bot = Bot(token=TOKEN, request_kwargs={"read_timeout": 20, "connect_timeout": 20})

feed = feedparser.parse(RSS_URL)
entries = feed.entries[:20]

def extract_images(description):
    return re.findall(r'<img src="([^"]+)"', description)

for entry in reversed(entries):
    text = entry.title
    description = entry.description
    images = extract_images(description)

    if len(images) > 1:
        media_group = []
        for i, img in enumerate(images):
            if i == 0:
                media_group.append(InputMediaPhoto(img, caption=text))
            else:
                media_group.append(InputMediaPhoto(img))
        bot.send_media_group(chat_id=CHANNEL_ID, media=media_group)
        time.sleep(1)

    elif len(images) == 1:
        bot.send_photo(chat_id=CHANNEL_ID, photo=images[0], caption=text)
        time.sleep(1)

    else:
        bot.send_message(chat_id=CHANNEL_ID, text=text)
        time.sleep(1)

print("✅ Done posting 20 tweets")
