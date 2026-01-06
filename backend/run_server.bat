@echo off
echo Starting RAG Chatbot backend server...
echo Make sure you have set up your .env file with the required API keys.
echo Server will be available at http://localhost:8000
echo Press Ctrl+C to stop the server.
echo.

REM Change to the backend directory
cd /d "%~dp0"

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate
) else (
    echo Warning: Virtual environment not found. Please run setup_and_run.bat first.
)

REM Run the backend server
python run_backend.py

pause