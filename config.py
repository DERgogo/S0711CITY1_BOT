import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "supersecret123")
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"

# Trage hier DEINE Railway-URL ein
WEBHOOK_URL = f"https://<dein-projektname>.up.railway.app{WEBHOOK_PATH}"
