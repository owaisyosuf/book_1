@echo off
echo Starting both backend and frontend servers...
echo.

echo Starting backend server on port 8000...
start cmd /k "cd /d G:\book_1\backend && python run_backend.py"

echo Starting frontend server on port 3000...
start cmd /k "cd /d G:\book_1 && npm run start"

echo.
echo Servers started!
echo - Backend: http://localhost:8000
echo - Frontend: http://localhost:3000
echo.
echo Close this window to stop both servers.
pause