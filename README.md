# FitBuddy - AI Fitness Plan Generator

Beginner-friendly FastAPI project with Gemini AI, Jinja2 HTML/CSS, and SQLite.

## Features
- Personalized 7-day workout plan
- AI nutrition tips
- Feedback-based plan update
- SQLite user storage
- View/delete users
- Local and cloud-ready configuration

## Run on Windows
```powershell
py -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```
Copy `.env.example` to `.env` and add your Gemini API key.

Start:
```powershell
.\venv\Scripts\python.exe run.py
```
Open http://127.0.0.1:8000

If no API key is supplied, the app uses built-in demo content so the project still runs.

## Render
Build command: `pip install -r requirements.txt`
Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
Add `GEMINI_API_KEY` in the hosting environment.

SQLite is suitable for learning/local use. Use a managed database for persistent production data.

This app is educational and not medical advice.
