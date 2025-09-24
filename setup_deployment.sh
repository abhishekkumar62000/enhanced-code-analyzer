#!/bin/bash
# Enhanced Code Analyzer - Deployment Setup Script
# This script installs necessary deployment tools for one-click deployment

echo "🚀 Enhanced Code Analyzer - Deployment Setup"
echo "============================================="
echo ""

# Check operating system
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    CYGWIN*)    MACHINE=Cygwin;;
    MINGW*)     MACHINE=MinGw;;
    *)          MACHINE="UNKNOWN:${OS}"
esac

echo "Detected OS: $MACHINE"
echo ""

# Install Node.js and npm if not present
echo "📦 Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    echo "Node.js not found. Please install Node.js from https://nodejs.org/"
    echo "This is required for Vercel CLI deployment."
else
    echo "✅ Node.js is installed: $(node --version)"
fi
echo ""

# Install Vercel CLI
echo "🔧 Installing Vercel CLI..."
if command -v npm &> /dev/null; then
    npm install -g vercel
    echo "✅ Vercel CLI installed successfully"
else
    echo "❌ npm not found. Install Node.js first."
fi
echo ""

# Install Heroku CLI
echo "🔧 Installing Heroku CLI..."
if [[ "$MACHINE" == "Linux" ]]; then
    curl https://cli-assets.heroku.com/install-ubuntu.sh | sh
elif [[ "$MACHINE" == "Mac" ]]; then
    if command -v brew &> /dev/null; then
        brew tap heroku/brew && brew install heroku
    else
        echo "Please install Homebrew first: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    fi
else
    echo "For Windows, download from: https://devcenter.heroku.com/articles/heroku-cli"
fi
echo ""

# Check Docker installation
echo "🐳 Checking Docker installation..."
if command -v docker &> /dev/null; then
    echo "✅ Docker is installed: $(docker --version)"
else
    echo "❌ Docker not found. Install from https://docs.docker.com/get-docker/"
fi
echo ""

# Install AWS CLI
echo "☁️  Installing AWS CLI..."
if [[ "$MACHINE" == "Linux" ]]; then
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
    rm -rf aws awscliv2.zip
elif [[ "$MACHINE" == "Mac" ]]; then
    if command -v brew &> /dev/null; then
        brew install awscli
    else
        echo "Please install Homebrew first"
    fi
else
    echo "For Windows, download from: https://aws.amazon.com/cli/"
fi
echo ""

# Install Git if not present
echo "📚 Checking Git installation..."
if ! command -v git &> /dev/null; then
    if [[ "$MACHINE" == "Linux" ]]; then
        sudo apt-get update && sudo apt-get install git -y
    elif [[ "$MACHINE" == "Mac" ]]; then
        if command -v brew &> /dev/null; then
            brew install git
        fi
    fi
    echo "✅ Git installed"
else
    echo "✅ Git is already installed: $(git --version)"
fi
echo ""

# Summary
echo "🎉 Deployment Setup Complete!"
echo "=============================="
echo "Available deployment platforms:"
echo ""
if command -v vercel &> /dev/null; then
    echo "✅ Vercel - Ready for deployment"
else
    echo "❌ Vercel - CLI not available"
fi

if command -v heroku &> /dev/null; then
    echo "✅ Heroku - Ready for deployment"  
else
    echo "❌ Heroku - CLI not available"
fi

if command -v docker &> /dev/null; then
    echo "✅ Docker - Ready for deployment"
else
    echo "❌ Docker - Not available"
fi

if command -v aws &> /dev/null; then
    echo "✅ AWS - Ready for deployment"
else
    echo "❌ AWS - CLI not available"
fi

echo ""
echo "🚀 You can now use the Enhanced Code Analyzer Deployment Hub!"
echo "Visit: http://localhost:8080/deployment-hub"
echo ""
echo "Manual deployment files will be generated if CLI tools are not available."
echo "The app will provide step-by-step instructions for manual deployment."