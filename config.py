import os

"""Konfiguration für den Telegram-Webhook.

Erklärung:
- `BOT_TOKEN` wird aus der Umgebung gelesen — niemals Secrets in Quellcode speichern.
- `WEBHOOK_PATH` und `WEBHOOK_URL` können per Env-Var überschrieben werden (praktisch für ngrok/tunnels).
"""

# Telegram Bot Token (aus Umgebungsvariablen, z.B. via CI/Platform secrets)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Secret für Telegram-Sicherheit: Pflichtfeld (kein schwaches Default mehr)
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
if not WEBHOOK_SECRET:
	raise RuntimeError("WEBHOOK_SECRET is required. Set the WEBHOOK_SECRET env var before running the application.")

# Webhook-Endpunkt: 1) nutze `WEBHOOK_PATH` Env-Var falls vorhanden, sonst aus BOT_TOKEN ableiten
if os.getenv("WEBHOOK_PATH"):
	WEBHOOK_PATH = os.getenv("WEBHOOK_PATH")
else:
	WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}" if BOT_TOKEN else "/webhook/undefined"

# Webhook-URL: erlaubt Override per Env-Var, sonst Fallback auf die (Railway-)Hostname + PATH
WEBHOOK_URL = os.getenv("WEBHOOK_URL") or f"https://s0711citybot.up.railway.app{WEBHOOK_PATH}"

if not BOT_TOKEN:
	# Warnung ausgeben — in CI/Prod empfiehlt sich ein Fail-fast Verhalten
	print("⚠️ WARNING: BOT_TOKEN is not set. Set the BOT_TOKEN env var before running the bot (main.py).")
