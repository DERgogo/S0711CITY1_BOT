import os

# Telegram Bot Token (kommt aus deiner .env-Datei)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Secret für Telegram-Sicherheit
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "s0711secret")

# Webhook-Endpunkt (Telegram ruft diesen Pfad auf)
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"

# ✅ Deine Railway-URL – hier eingetragen
WEBHOOK_URL = f"https://s0711citybot.up.railway.app{WEBHOOK_PATH}"
