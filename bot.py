from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Einfacher /start Handler mit 0711-Text."""
    text = (
        "🟣 S0711CITYBOT® online.\n\n"
        "0711 Vibes. City Info. Echt Stuggi.\n"
        "Schreib /help für mehr."
    )
    if update.message:
        await update.message.reply_text(text)


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "📖 Befehle:\n"
        "/start – Willkommen & Intro\n"
        "/help – Diese Hilfe\n"
    )
    if update.message:
        await update.message.reply_text(text)


def build_application(bot_token: str) -> Application:
    """Erstellt die Telegram Application mit allen Handlern."""
    app = ApplicationBuilder().token(bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))

    return app
