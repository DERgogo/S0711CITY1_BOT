import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "supersecret123")
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"

# ❗ Hier die **echte Railway-URL** deines Projekts eintragen:
WEBHOOK_URL = f"https://<DEIN_PROJEKT>.up.railway.app{WEBHOOK_PATH}"
