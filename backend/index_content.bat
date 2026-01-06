@echo off
echo Indexing book content into the vector store...
echo This will index all markdown files from the docs directory.
echo.

REM Change to the backend directory
cd /d "%~dp0"

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate
) else (
    echo Warning: Virtual environment not found. Please run setup_and_run.bat first.
)

REM Run the content indexing script
python index_book_content.py

echo.
echo Content indexing complete!
pause