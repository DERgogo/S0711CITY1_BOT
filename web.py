@fastapi_app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    """Wird von Telegram aufgerufen, wenn eine neue Nachricht kommt."""
    data = await request.json()

    # 👀 Logge den JSON-Inhalt der Nachricht (nur für dich!)
    print("📩 Eingehendes Telegram-Update:", data)

    # Telegram-Update verarbeiten
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"ok": True}
