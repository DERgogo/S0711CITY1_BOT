import asyncio
import uvicorn

from config import WEBHOOK_URL
from web import fastapi_app, telegram_app


async def set_webhook() -> None:
    """Setzt den Telegram Webhook auf die Railway-URL."""
    await telegram_app.bot.set_webhook(WEBHOOK_URL)
    print("✅ Webhook gesetzt auf:", WEBHOOK_URL)


def main() -> None:
    # Webhook einmalig setzen
    asyncio.run(set_webhook())

    # FastAPI + Uvicorn starten
    uvicorn.run(
        "web:fastapi_app",
        host="0.0.0.0",
        port=8080,
    )


if __name__ == "__main__":
    main()
