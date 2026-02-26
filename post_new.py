import os
import json
import time
import re
import feedparser
from telegram import Bot, InputMediaPhoto

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]
RSS_URL = os.environ["RSS_URL"]

bot = Bot(token=TOKEN)

feed = feedparser.parse(RSS_URL)
entries = feed.entries

def extract_images(description):
    return re.findall(r'<img src="([^"]+)"', description)

with open("posted.json", "r") as f:
    posted_ids = json.load(f)

updated_ids = posted_ids.copy()

for entry in reversed(entries):
    tweet_id = entry.id

    if tweet_id in posted_ids:
        continue

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

    elif len(images) == 1:
        bot.send_photo(chat_id=CHANNEL_ID, photo=images[0], caption=text)

    else:
        bot.send_message(chat_id=CHANNEL_ID, text=text)

    updated_ids.append(tweet_id)
    time.sleep(1)

updated_ids = updated_ids[-200:]

with open("posted.json", "w") as f:
    json.dump(updated_ids, f)

print("✅ Done checking new tweets")