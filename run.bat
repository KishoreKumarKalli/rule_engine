@echo off
echo Setting up Python environment...

REM Create virtual environment if it doesn't exist
if not exist venv (
    python -m venv venv
    echo Created virtual environment
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install requirements
pip install -r requirements.txt

REM Create static directory if it doesn't exist
if not exist static mkdir static

REM Run the application
python -m uvicorn app:app --reload

pause