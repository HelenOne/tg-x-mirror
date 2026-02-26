import os
import feedparser
from telegram import Bot
from telegram import InputMediaPhoto

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]
RSS_URL = os.environ["RSS_URL"]

bot = Bot(token=TOKEN)

feed = feedparser.parse(RSS_URL)

entries = feed.entries[:20]

for entry in reversed(entries):
    text = entry.title
    media = entry.get("media_content", [])

    if len(media) > 1:
        media_group = []
        for i, item in enumerate(media):
            if i == 0:
                media_group.append(InputMediaPhoto(item["url"], caption=text))
            else:
                media_group.append(InputMediaPhoto(item["url"]))
        bot.send_media_group(chat_id=CHANNEL_ID, media=media_group)

    elif len(media) == 1:
        bot.send_photo(chat_id=CHANNEL_ID, photo=media[0]["url"], caption=text)

    else:
        bot.send_message(chat_id=CHANNEL_ID, text=text)

print("✅ Done posting 20 tweets")