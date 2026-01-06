@echo off
echo Setting up RAG Chatbot for AI/Spec-Driven Book...

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo Installing backend dependencies...
cd /d "%~dp0"
pip install -r requirements.txt

echo.
echo Environment setup complete!
echo.
echo To run the backend server:
echo   1. Update the .env file with your API keys
echo   2. Run: python -m uvicorn main:app --reload --port 8000
echo.
echo To index your book content, run: python index_book_content.py
echo.
echo Setup complete!
pause