import asyncio
import uvicorn

from config import WEBHOOK_URL, WEBHOOK_SECRET
from web import fastapi_app, telegram_app


async def set_webhook() -> None:
    """Setzt den Telegram Webhook auf die Railway-URL mit Secret."""
    await telegram_app.bot.set_webhook(
        WEBHOOK_URL,
        secret_token=WEBHOOK_SECRET,
        allowed_updates=["message", "callback_query"]
    )
    print("✅ Webhook gesetzt auf:", WEBHOOK_URL)


def main() -> None:
    asyncio.run(set_webhook())

    uvicorn.run(
        "web:fastapi_app",
        host="0.0.0.0",
        port=8080,
    )


if __name__ == "__main__":
    main()
