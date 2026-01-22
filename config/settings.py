import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

if not BOT_TOKEN or not ALPHA_VANTAGE_API_KEY:
    raise ValueError("Не заданы переменные окружения")
