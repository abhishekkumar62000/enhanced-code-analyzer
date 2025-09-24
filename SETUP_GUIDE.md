# 🚀 **Easy Setup Guide for Source Code Analysis AI**

## ✅ **Quick Start (Recommended)**

### **Option 1: Simple Version (Works immediately)**
```bash
python simple_app.py
```
Then open: http://localhost:8080

### **Option 2: Full Version with Vector Database**
```bash
# Run the batch file
run_app.bat
```

---

## 📋 **What's Already Done ✅**

- ✅ OpenAI API key configured in `.env`
- ✅ Python dependencies installed
- ✅ Flask app ready to run
- ✅ Simple version working without complex dependencies

---

## 🎯 **How to Use Your App**

### **Step 1**: Start the Application
```bash
python simple_app.py
```

### **Step 2**: Open Your Browser
Go to: **http://localhost:8080**

### **Step 3**: Input a GitHub Repository
- Enter any public GitHub repository URL (e.g., `https://github.com/username/repo-name`)
- Click "Send"
- Wait for confirmation message

### **Step 4**: Ask Questions About the Code
- Type questions like:
  - "What does this code do?"
  - "Explain the main functions"
  - "How does the authentication work?"
  - "What are the dependencies?"

### **Step 5**: Clear Data (if needed)
- Type `clear` to reset the loaded code

---

## 🔧 **Troubleshooting**

### **If you get API errors:**
1. Check your `.env` file has the correct OpenAI API key
2. Ensure you have internet connection
3. Verify your OpenAI account has credits

### **If repository loading fails:**
1. Make sure the repository is public
2. Check the URL format: `https://github.com/username/repo-name`
3. Ensure you have internet connection

### **If the app won't start:**
1. Make sure you're in the correct directory
2. Run: `pip install flask python-dotenv gitpython openai==0.28`
3. Check that port 8080 is not being used by another application

---

## 🎨 **Features Available**

- 🔗 **GitHub Repository Loading**: Clone and analyze any public repo
- 🤖 **AI-Powered Analysis**: Ask natural language questions about code
- 🔍 **Python Code Focus**: Specifically analyzes Python files
- 💬 **Interactive Chat**: Conversational interface for code exploration
- 🗑️ **Clear Function**: Reset loaded content with `clear` command

---

## 📊 **What Each File Does**

- **`simple_app.py`** - Simplified working version (recommended)
- **`app.py`** - Full version with vector database
- **`store_index.py`** - Creates embeddings for the full version
- **`templates/index.html`** - Web interface
- **`.env`** - Contains your OpenAI API key
- **`run_app.bat`** - Windows batch script for easy startup

---

## 🎉 **You're Ready to Go!**

Your Source Code Analysis AI is now ready to use. Simply run `python simple_app.py` and start analyzing code repositories with AI assistance!