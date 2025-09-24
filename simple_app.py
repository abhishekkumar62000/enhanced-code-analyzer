from flask import Flask, render_template, jsonify, request
import os
from dotenv import load_dotenv
from openai import OpenAI
from git import Repo
import tempfile
import shutil

app = Flask(__name__)

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

# Simple in-memory storage for code content
code_content = ""

def clone_and_read_repo(repo_url):
    """Clone repository and read Python files"""
    global code_content
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    repo_path = os.path.join(temp_dir, "repo")
    
    try:
        # Clone repository
        Repo.clone_from(repo_url, repo_path)
        
        # Read Python files
        content = []
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            relative_path = os.path.relpath(file_path, repo_path)
                            content.append(f"=== {relative_path} ===\n{f.read()}\n\n")
                    except Exception as e:
                        content.append(f"=== {relative_path} ===\nError reading file: {str(e)}\n\n")
        
        code_content = "\n".join(content)
        return True, f"Successfully loaded {len([c for c in content if not c.startswith('Error')])} Python files"
        
    except Exception as e:
        return False, f"Error processing repository: {str(e)}"
    finally:
        # Clean up temporary directory
        try:
            shutil.rmtree(temp_dir)
        except:
            pass

def ask_openai(question, context):
    """Ask OpenAI about the code"""
    try:
        # Truncate context if too long (OpenAI has token limits)
        max_context_length = 8000
        if len(context) > max_context_length:
            context = context[:max_context_length] + "\n\n[Content truncated due to length]"
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes source code. Answer questions about the provided code context."},
                {"role": "user", "content": f"Code Context:\n{context}\n\nQuestion: {question}"}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error getting AI response: {str(e)}"

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')

@app.route('/chatbot', methods=["GET", "POST"])
def gitRepo():
    if request.method == 'POST':
        user_input = request.form['question']
        
        if user_input.strip():
            success, message = clone_and_read_repo(user_input)
            if success:
                return jsonify({"response": f"✅ {message}. You can now ask questions about the code!"})
            else:
                return jsonify({"response": f"❌ {message}"})
        else:
            return jsonify({"response": "Please provide a valid GitHub repository URL."})
    
    return jsonify({"response": "Please provide a GitHub repository URL."})

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    
    if msg.lower() == "clear":
        global code_content
        code_content = ""
        return "🗑️ Code content cleared."
    
    if not code_content:
        return "📝 Please first load a repository using the form above."
    
    # Get AI response
    response = ask_openai(msg, code_content)
    return response

if __name__ == '__main__':
    print("🚀 Starting Source Code Analysis AI...")
    print("📱 Open your browser and go to: http://localhost:8080")
    app.run(host="0.0.0.0", port=8080, debug=True)