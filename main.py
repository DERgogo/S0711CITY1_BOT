import uvicorn
import asyncio
from app.web import fastapi_app, telegram_app
from app.config import WEBHOOK_URL

async def on_startup():
    await telegram_app.bot.set_webhook(WEBHOOK_URL)
    print("Webhook gesetzt:", WEBHOOK_URL)

def run():
    uvicorn.run(
        fastapi_app,
        host="0.0.0.0",
        port=8080
    )

if __name__ == "__main__":
    asyncio.run(on_startup())
    run()
