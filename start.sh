#!/bin/bash
python3 -m uvicorn app.web:fastapi_app --host 0.0.0.0 --port 8080
