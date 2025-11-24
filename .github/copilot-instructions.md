<!-- .github/copilot-instructions.md for S0711CITY1_BOT -->
# Hinweise für AI-Coding-Agenten (S0711CITY1_BOT)

Kurzer Überblick
- **Architektur:** FastAPI-Webservice (`web.py`) hostet einen Telegram-Webhook; die Telegram-Application wird in `bot.py` erzeugt und in `web.py` als `telegram_app` eingebunden. `main.py` setzt zusätzlich den Telegram-Webhook (per `telegram_app.bot.set_webhook`) und startet `uvicorn`.
- **Warum so:** Projekt ist für Hosting auf Railway/Heroku-artigen Diensten gedacht — Webhook-basiertes Bot-Modell statt Long-Polling.

Wichtige Dateien
- `bot.py`: Erzeugt `Application` und registriert Handler (`CommandHandler`). Erweiterungen an diesem Bot erfolgen durch Hinzufügen weiterer Handler an `build_application()`.
- `web.py`: FastAPI-App mit Endpoints `/`, `/ping` und dem POST-Webhook-Handler (`WEBHOOK_PATH`). Prüft Header `X-Telegram-Secret` gegen `WEBHOOK_SECRET`.
- `main.py`: `set_webhook()` ruft `telegram_app.bot.set_webhook(WEBHOOK_URL, secret_token=WEBHOOK_SECRET, allowed_updates=[...])` auf, dann startet `uvicorn`.
- `config.py`: Zentrale Konfigurationsquelle — liest `BOT_TOKEN`, `WEBHOOK_SECRET` und bildet `WEBHOOK_PATH`/`WEBHOOK_URL`. Achtung: `WEBHOOK_PATH` enthält `BOT_TOKEN`.
- `start.sh` / `Procfile`: Start-Skripte / Prozessdeklaration für Deployment (z.B. Railway).
- `requirements.txt`: Abhängigkeiten; wichtig: `python-telegram-bot[fastapi]>=20.0` erwartet die v20 API.

Run & Dev-Workflow (konkrete Befehle)
- Lokales Starten (öffentliche URL erforderlich für Webhooks):
```bash
export BOT_TOKEN="<dein-token>"
export WEBHOOK_SECRET="meinsecret"
export WEBHOOK_URL="https://<your-public-url>/webhook/$BOT_TOKEN"
python main.py
```
- Alternativ (Hot reload, nur FastAPI ohne Webhook-Setzen — nützlich beim Entwickeln von Endpoints):
```bash
export BOT_TOKEN="<dein-token>" # nötig, da config.py BOT_TOKEN nutzt
export WEBHOOK_SECRET="meinsecret"
uvicorn web:fastapi_app --reload --host 0.0.0.0 --port 8080
```
- Railway / Deploy: `Procfile` enthält `web: python main.py`. Setze env-vars in Railway: `BOT_TOKEN`, `WEBHOOK_SECRET`, optional `WEBHOOK_URL`.

Security / Gotchas
- `WEBHOOK_PATH` wird aus `BOT_TOKEN` erzeugt. Wenn `BOT_TOKEN` fehlt, kann der Pfad `None` enthalten — stelle sicher, dass `BOT_TOKEN` gesetzt ist.
- Der FastAPI-Webhook prüft Header `X-Telegram-Secret`. Beim Setzen des Webhooks muss `secret_token` mit `WEBHOOK_SECRET` übereinstimmen.
- `main.py` setzt den Webhook bei Start automatisch. Beim Entwickeln lokal solltest du entweder eine öffentliche URL (ngrok, Cloudflare Tunnel) verwenden oder `main.py` modifizieren, um das Setzen zu überspringen.

Code-Patterns & Konventionen
- Handler-Registrierung: `app.add_handler(CommandHandler("start", start))` in `bot.py`. Folge dem Muster beim Hinzufügen von Callback-, Message- oder Conversation-Handlern.
- Logging: Projekt nutzt primitiv `print()`-Statements (z.B. in `web.py`). Bei größeren Änderungen bevorzugen: `logging`-Modul, aber respektiere bestehende einfache Ausgabeweise bei schnellen PRs.
- Typen: Asynchrone Handler (`async def`) und `telegram.ext.Application`-API (v20). Verwende `ContextTypes.DEFAULT_TYPE` für Context-Argumente.

Integrationspunkte
- Telegram API: `telegram_app.bot.set_webhook(...)` und `telegram_app.process_update(update)` in `web.py`.
- Deployment: Railway/Heroku-Style via `Procfile`; CI/CD nicht Teil des Repo.

```markdown
<!-- Condensed Copilot instructions for S0711CITY1_BOT -->
## Kurz — schnell produktiv
- Architektur: FastAPI (`web.py`) empfängt Telegram-Webhooks; `bot.py` baut die `Application` (Handler), `main.py` setzt Webhook und startet `uvicorn`.
- Ziel: Deployment auf Railway/Heroku‑ähnlichen Plattformen (Webhook statt Long‑polling).

## Dateien, die AI-Agenten oft ändern
- `bot.py` — zentral: `build_application()` registriert Handler (z.B. `CommandHandler("start", start)`).
- `web.py` — FastAPI app; enthält POST-Webhook-Handler, prüft `X-Telegram-Secret` gegen `WEBHOOK_SECRET`.
- `main.py` — setzt Webhook per `telegram_app.bot.set_webhook(WEBHOOK_URL, secret_token=WEBHOOK_SECRET, ...)` und startet `uvicorn`.
- `config.py` — liest `BOT_TOKEN`, `WEBHOOK_SECRET`, erzeugt `WEBHOOK_PATH` (enthält `BOT_TOKEN`) und `WEBHOOK_URL`.
- `requirements.txt`, `Procfile`, `start.sh` — Deployment / Start‑scripts.

## Konkrete Befehle (kopierbar)
Lokaler Start (Webhooks — benötigt öffentliche URL):
```bash
export BOT_TOKEN="<dein-token>"
export WEBHOOK_SECRET="meinsecret"
export WEBHOOK_URL="https://<public>/webhook/$BOT_TOKEN"
python main.py
```
Entwickeln nur FastAPI (kein Webhook-Setzen):
```bash
export BOT_TOKEN="<dein-token>" # config.py benötigt BOT_TOKEN
uvicorn web:fastapi_app --reload --host 0.0.0.0 --port 8080
```

## Projekt-spezifische Patterns / Gotchas
- `WEBHOOK_PATH` enthält `BOT_TOKEN`. Fehlt `BOT_TOKEN`, resultiert ein ungültiger Pfad — setze env vars.
- Webhook-Sicherheit: Header `X-Telegram-Secret` muss mit `WEBHOOK_SECRET` übereinstimmen (siehe `web.py`).
- API-Version: Projekt nutzt `python-telegram-bot` v20+ (Async API, `Application`, `ContextTypes.DEFAULT_TYPE`). Verwende asynchrone Handler (`async def`) und die v20 handler-APIs.
- Logging ist minimal (häufig `print()`); vermeide große Refactors von Logging in kleinen PRs.

## Where to make changes
- Neue Bot-Features: füge Handler in `bot.py::build_application()` hinzu; exportiere Helper-Funktionen neben Handlers.
- HTTP‑Endpoints: Ergänze Routen in `web.py`; respektiere die Header‑Prüfung für webhook‑POSTs.
- Wenn du Webhook‑Pfad/URL-Logik änderst: dokumentiere Env‑Var‑Auswirkung (`BOT_TOKEN`, `WEBHOOK_URL`, `WEBHOOK_SECRET`) und aktualisiere `README.md`.

## Quick examples (code-locations)
- Handler registration: `bot.py` — search for `add_handler` or `CommandHandler("start"`.
- Webhook entry: `web.py` — search for `process_update` / `X-Telegram-Secret`.
- Webapp entrypoint: `main.py` — `set_webhook()` + `uvicorn` call.

## Feedback
Wenn etwas fehlt (z. B. ConversationHandler‑Beispiel, ngrok‑debug recipe oder ausführliche Tests), sag mir welche Sektion ich erweitern soll.
```
