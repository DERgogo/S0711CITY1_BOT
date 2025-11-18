from telegram.ext import ApplicationBuilder
from app.config import BOT_TOKEN

telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()
