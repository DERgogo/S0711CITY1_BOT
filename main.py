from app.web import fastapi_app, telegram_app
import uvicorn
from app.config import WEBHOOK_URL

async def start_webhook():
    await telegram_app.bot.set_webhook(WEBHOOK_URL)

if __name__ == "__main__":
    import asyncio
    asyncio.run(start_webhook())
    uvicorn.run("app.web:fastapi_app", host="0.0.0.0", port=8000)
