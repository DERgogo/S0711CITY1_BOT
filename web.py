from fastapi import FastAPI, Request, HTTPException
from telegram import Update
from telegram.ext import Application

from config import BOT_TOKEN, WEBHOOK_PATH, WEBHOOK_SECRET
from bot import build_application

telegram_app: Application = build_application(BOT_TOKEN)
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
    return {"status": "running", "token_suffix": BOT_TOKEN[-5:]}

@fastapi_app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    # Secret prüfen
    secret = request.headers.get("X-Telegram-Secret")
    if secret != WEBHOOK_SECRET:
        print("⛔ Ungültiger Zugriff – Secret fehlt oder falsch!")
        raise HTTPException(status_code=403, detail="Forbidden")

    data = await request.json()
    print("📩 Telegram-Update:", data)

    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"ok": True}
