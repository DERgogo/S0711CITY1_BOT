import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "DEIN_TELEGRAM_BOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "supersecret123")
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBHOOK_URL = f"https://deinprojekt-url{WEBHOOK_PATH}"
