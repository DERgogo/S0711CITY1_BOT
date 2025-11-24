from fastapi import FastAPI, Request, HTTPException
from telegram import Update
from telegram.ext import Application

from config import BOT_TOKEN, WEBHOOK_PATH, WEBHOOK_SECRET
from bot import build_application

# Telegram-Bot-Instanz mit Handlers (nur erzeugen, wenn BOT_TOKEN gesetzt)
telegram_app: Application | None
if BOT_TOKEN:
    try:
        telegram_app = build_application(BOT_TOKEN)
    except Exception as e:
        print(f"Failed to build Telegram application: {e}")
        telegram_app = None
else:
    telegram_app = None

# FastAPI-Anwendung
fastapi_app = FastAPI()


@fastapi_app.get("/")
async def root():
    return {
        "status": "ok",
        "bot": "S0711CITYBOT",
        "webhook": WEBHOOK_PATH
    }


@fastapi_app.get("/ping")
async def ping():
    # Aus Sicherheitsgründen geben wir keinen Token-Suffix mehr zurück.
    return {"status": "running"}


@fastapi_app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    """Verarbeitet eingehende Telegram Webhook-POSTs."""
    if telegram_app is None:
        # Kein Bot-Token gesetzt / App nicht initialisiert
        raise HTTPException(status_code=503, detail="Telegram application not configured (BOT_TOKEN missing)")
    # Sicherheit: Secret-Header prüfen
    secret = request.headers.get("X-Telegram-Secret")
    if secret != WEBHOOK_SECRET:
        print("⛔ Ungültiger Zugriff – Secret fehlt oder falsch!")
        raise HTTPException(status_code=403, detail="Forbidden")

    # Telegram-Update verarbeiten
    data = await request.json()
    print("📩 Telegram-Update:", data)

    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"ok": True}
