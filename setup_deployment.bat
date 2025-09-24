@echo off
REM Enhanced Code Analyzer - Deployment Setup Script for Windows
REM This script helps install necessary deployment tools

echo ================================
echo 🚀 Enhanced Code Analyzer Setup  
echo ================================
echo.

echo 📦 Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Node.js is installed
    node --version
) else (
    echo ❌ Node.js not found
    echo Please download and install from: https://nodejs.org/
    echo This is required for Vercel CLI deployment.
    pause
)
echo.

echo 🔧 Installing Vercel CLI...
npm --version >nul 2>&1
if %errorlevel% equ 0 (
    npm install -g vercel
    echo ✅ Vercel CLI installation attempted
) else (
    echo ❌ npm not found. Install Node.js first.
)
echo.

echo 🔧 Checking Heroku CLI...
heroku --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Heroku CLI is installed
) else (
    echo ❌ Heroku CLI not found
    echo Download from: https://devcenter.heroku.com/articles/heroku-cli
)
echo.

echo 🐳 Checking Docker...
docker --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Docker is installed
    docker --version
) else (
    echo ❌ Docker not found
    echo Download from: https://docs.docker.com/desktop/windows/install/
)
echo.

echo ☁️ Checking AWS CLI...
aws --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ AWS CLI is installed
) else (
    echo ❌ AWS CLI not found
    echo Download from: https://aws.amazon.com/cli/
)
echo.

echo 📚 Checking Git...
git --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Git is installed
    git --version
) else (
    echo ❌ Git not found
    echo Download from: https://git-scm.com/download/win
)
echo.

echo ============================
echo 🎉 Setup Check Complete!
echo ============================
echo.
echo Available deployment options:
echo.

vercel --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Vercel - Ready for deployment
) else (
    echo ❌ Vercel - Install Node.js and run: npm install -g vercel
)

heroku --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Heroku - Ready for deployment
) else (
    echo ❌ Heroku - Download CLI from heroku.com
)

docker --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Docker - Ready for deployment
) else (
    echo ❌ Docker - Install Docker Desktop
)

aws --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ AWS - Ready for deployment
) else (
    echo ❌ AWS - Install AWS CLI
)

echo.
echo 🚀 Your Enhanced Code Analyzer Deployment Hub is ready!
echo Visit: http://localhost:8080/deployment-hub
echo.
echo 💡 Don't worry if some tools are missing - the app will generate
echo    configuration files and provide manual deployment instructions!
echo.
pause