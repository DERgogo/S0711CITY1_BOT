from fastapi import FastAPI, Request
from telegram import Update
from app.bot import telegram_app

fastapi_app = FastAPI()

@fastapi_app.post("/")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"status": "ok"}
