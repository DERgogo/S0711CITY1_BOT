import os

# Telegram Bot Token aus Railway (BOT_TOKEN)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Basis-URL deiner Railway-App, z.B. https://web-production-5cd20.up.railway.app
APP_URL = os.getenv("APP_URL")

# Pfad, unter dem Telegram den Webhook aufruft
WEBHOOK_PATH = "/webhook"

# Vollständige Webhook-URL:
# Entweder direkt aus WEBHOOK_URL oder aus APP_URL + /webhook gebaut
WEBHOOK_URL = os.getenv("WEBHOOK_URL") or f"{APP_URL.rstrip('/')}{WEBHOOK_PATH}"

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN ist nicht gesetzt")
if not APP_URL:
    raise RuntimeError("APP_URL ist nicht gesetzt")
