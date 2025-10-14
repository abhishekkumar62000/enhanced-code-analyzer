@echo off
echo ================================
echo Source Code Analysis AI Setup
echo ================================ 

echo Step 1: Checking if .env file exists...
if not exist .env (
    echo ERROR: .env file not found!
    echo Please create a .env file with your OPENAI_API_KEY
    echo Example: OPENAI_API_KEY="your-api-key-here"
    pause
    exit /b 1
)

echo Step 2: Installing required packages...
pip install langchain-community langchain-openai langchain-text-splitters flask python-dotenv gitpython

echo Step 3: Starting the application...
echo.
echo ================================
echo Application is starting...
echo Open your browser and go to: http://localhost:8080
echo ================================
echo.

python app.py

pause
