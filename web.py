from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import ApplicationBuilder
from app.config import BOT_TOKEN
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()
fastapi_app = FastAPI()
@fastapi_app.post('/')
async def webhook(req:Request):
    data=await req.json()
    update=Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {'status':'ok'}
