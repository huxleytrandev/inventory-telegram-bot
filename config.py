import os
from dotenv import load_dotenv

load_dotenv()

SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE")
TELEGRAM_URL_BASE = os.getenv("TELEGRAM_URL_BASE")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID_BOT = os.getenv("TELEGRAM_CHAT_ID_BOT")