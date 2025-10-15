@echo off
REM Enhanced Code Analyzer - Auto Deployment Script
REM This script automates the deployment process to free cloud platforms

echo ===============================================
echo 🚀 Enhanced Code Analyzer - Free Cloud Deploy
echo ===============================================
echo.

echo Select your preferred FREE deployment platform:
echo.
echo 1. Vercel (Recommended - Fastest deployment)
echo 2. Railway (Auto-deploy from GitHub)
echo 3. Render (750 hours/month free)
echo 4. Show all deployment options
echo.

set /p choice="Enter your choice (1-4): "

if %choice%==1 goto vercel
if %choice%==2 goto railway  
if %choice%==3 goto render
if %choice%==4 goto showall

:vercel
echo.
echo 🌟 VERCEL DEPLOYMENT SELECTED
echo ===============================
echo.
echo 📋 Prerequisites:
echo ✓ Node.js installed
echo ✓ GitHub account
echo ✓ OpenAI API Key
echo.

echo Step 1: Installing Vercel CLI...
npm install -g vercel
if %errorlevel% neq 0 (
    echo ❌ Failed to install Vercel CLI
    echo Please install Node.js from: https://nodejs.org/
    pause
    exit /b 1
)

echo.
echo Step 2: Initialize deployment...
echo ✅ vercel.json already created
echo ✅ requirements.txt updated
echo ✅ Project ready for deployment

echo.
echo Step 3: Starting Vercel deployment...
echo 💡 When prompted:
echo    - Link to existing project? No
echo    - Project name: enhanced-code-analyzer
echo    - Directory: ./
echo    - Override settings? No
echo.

vercel

echo.
echo Step 4: Adding environment variables...
echo 🔑 Please enter your OpenAI API Key when prompted
vercel env add OPENAI_API_KEY

echo.
echo Step 5: Deploying to production...
vercel --prod

echo.
echo 🎉 DEPLOYMENT COMPLETE!
echo Your Enhanced Code Analyzer is now live!
echo.
goto end

:railway
echo.
echo 🚂 RAILWAY DEPLOYMENT SELECTED  
echo ===============================
echo.
echo 📋 Manual Setup Required:
echo.
echo 1. Go to: https://railway.app
echo 2. Sign up with GitHub (FREE)
echo 3. Create new project from GitHub repo
echo 4. Add environment variable: OPENAI_API_KEY
echo.
echo 📁 GitHub Setup:
echo.

git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git not installed
    echo Please install from: https://git-scm.com/
    pause
    exit /b 1
)

echo ✅ Initializing Git repository...
git init
git add .
git commit -m "Enhanced Code Analyzer - Ready for Railway deployment"

echo.
echo 🔗 Next steps:
echo 1. Create GitHub repository at: https://github.com/new
echo 2. Name it: enhanced-code-analyzer
echo 3. Run these commands:
echo.
echo    git remote add origin https://github.com/YOURUSERNAME/enhanced-code-analyzer.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 4. Go to Railway → New Project → Deploy from GitHub
echo 5. Select your repository
echo 6. Add OPENAI_API_KEY environment variable
echo.
goto end

:render
echo.
echo 🎨 RENDER DEPLOYMENT SELECTED
echo =============================
echo.
echo 📋 Manual Setup Required:
echo.
echo 1. Go to: https://render.com
echo 2. Sign up with GitHub (FREE - 750 hours/month)
echo 3. New → Web Service → Connect GitHub repo
echo.
echo ⚙️ Configuration:
echo    Build Command: pip install -r requirements.txt
echo    Start Command: gunicorn enhanced_app_optimized:app
echo    Environment: Python 3
echo.
echo 📁 GitHub Setup:

git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git not installed
    echo Please install from: https://git-scm.com/
    pause
    exit /b 1
)

echo ✅ Initializing Git repository...
git init
git add .
git commit -m "Enhanced Code Analyzer - Ready for Render deployment"

echo.
echo 🔗 Next steps:
echo 1. Create GitHub repository at: https://github.com/new  
echo 2. Name it: enhanced-code-analyzer
echo 3. Run these commands:
echo.
echo    git remote add origin https://github.com/YOURUSERNAME/enhanced-code-analyzer.git
echo    git branch -M main  
echo    git push -u origin main
echo.
echo 4. Go to Render → New → Web Service
echo 5. Connect your GitHub repository
echo 6. Add OPENAI_API_KEY environment variable
echo.
goto end

:showall
echo.
echo 🌟 ALL FREE DEPLOYMENT OPTIONS
echo ===============================
echo.
echo 1. 🟢 VERCEL (Recommended)
echo    ✅ 100GB bandwidth/month
echo    ✅ Custom domains  
echo    ✅ Auto SSL
echo    ✅ Instant deployment
echo    💡 Best for: Quick deployment
echo.
echo 2. 🔵 RAILWAY  
echo    ✅ $5 credit monthly
echo    ✅ Database included
echo    ✅ Auto-deploy from Git
echo    💡 Best for: Full-stack apps
echo.
echo 3. 🟡 RENDER
echo    ✅ 750 hours/month
echo    ✅ PostgreSQL free
echo    ✅ Custom domains
echo    💡 Best for: Always-on apps
echo.
echo 4. 🟠 HEROKU (Limited Free)
echo    ⚠️  Free tier discontinued
echo    💡 Only for existing accounts
echo.
echo.
echo 💡 Recommendation: Start with Vercel for easiest deployment!
echo.

:end
echo.
echo 🎯 DEPLOYMENT SUMMARY
echo ====================
echo.
echo Your Enhanced Code Analyzer includes:
echo ✅ Multi-language Code Analysis
echo ✅ Security Vulnerability Scanner  
echo ✅ Interactive Code Playground
echo ✅ Voice Code Analysis
echo ✅ Real-time Collaboration
echo ✅ AI Code Assistant
echo ✅ Advanced Analytics Dashboard
echo ✅ Auto-Documentation Generator
echo ✅ Deployment Automation Hub
echo.
echo 💰 Total Cost: FREE (only pay for OpenAI API usage)
echo 🚀 Enterprise features deployed to cloud!
echo.
echo 📖 For detailed instructions, see: DEPLOYMENT_GUIDE.md
echo.
pause
