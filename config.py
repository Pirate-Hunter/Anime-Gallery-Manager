import os
from telethon import TelegramClient

api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
bot_token = os.environ.get('BOT_TOKEN')
database_url = os.environ.get("DATABASE_URL")
main_group_id = os.environ.get("MAIN_GROUP_ID")
bot_id = os.environ.get("BOT_ID")

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)