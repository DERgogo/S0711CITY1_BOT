from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application

from config import BOT_TOKEN, WEBHOOK_PATH
from bot import build_application

# Telegram-Application
telegram_app: Application = build_application(BOT_TOKEN)

# FastAPI-App
fastapi_app = FastAPI()


@fastapi_app.get("/")
async def root():
    return {"status": "ok", "bot": "S0711CITYBOT", "webhook": WEBHOOK_PATH}


@fastapi_app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    """Wird von Telegram aufgerufen, wenn eine neue Nachricht kommt."""
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"ok": True}
