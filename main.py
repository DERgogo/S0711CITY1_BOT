import uvicorn
from app.web import fastapi_app, telegram_app
from app.config import WEBHOOK_URL
import asyncio
async def on_startup():
    await telegram_app.bot.set_webhook(WEBHOOK_URL)
if __name__=='__main__':
    asyncio.run(on_startup())
    uvicorn.run(fastapi_app,host='0.0.0.0',port=8080)
