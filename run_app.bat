@echo off
echo Starting KrishiAI+ Backend and Frontend...

:: Start the backend in a new window using SQLite local DB
start "KrishiAI Backend" cmd /c "set DATABASE_URL=sqlite:///./krishiai.db && venv\Scripts\python.exe -m uvicorn krishiai.main:app --workers 1 --reload"

:: Start the frontend in a new window
start "KrishiAI Frontend" cmd /c "cd frontend && npm run dev"

echo Both services have been started in separate windows!
echo The frontend will be available at http://localhost:5173
echo The backend API will be available at http://127.0.0.1:8000
