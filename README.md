# S0711CITY FULL BOT

Future0711Y / S0711CITY Bot mit:
- Webhook (FastAPI + python-telegram-bot 20.6)
- Premium Onboarding (3 Schritte, Buttons, 0711-Vibes)
- XP-System (Level, Achievements, Leaderboard)
- Daily Quests
- 0711 Shop (XP -> Items)
- Casino / Slot
- Duelle
- City / Media / Grow / Türsteher-Module (Stub)

## Deployment (kurz)

1. Repo auf GitHub erstellen.
2. ZIP entpacken und Inhalt ins Repo hochladen.
3. Auf Railway neues Projekt -> Deploy from GitHub.
4. In Railway unter Variables setzen:
   - BOT_TOKEN = dein Bot Token von BotFather
   - WEBHOOK_URL = https://DEIN-SERVICE.up.railway.app/
5. Deploy starten.
6. In Telegram: /start an deinen Bot schicken.
