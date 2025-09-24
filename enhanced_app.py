from flask import Flask, render_template, jsonify, request, send_file
import os
from dotenv import load_dotenv
from openai import OpenAI
from git import Repo
import tempfile
import shutil
import json
import ast
import subprocess
import sys
from collections import defaultdict, Counter
import re
from datetime import datetime
import io
import contextlib

app = Flask(__na            code_content += "\\n[Truncated...]"
        
        full_context = "\\n".join(context_parts) + code_content
        
        # Truncate if too long (COST OPTIMIZED)
        if len(full_context) > MAX_CONTEXT_LENGTH:
            full_context = full_context[:MAX_CONTEXT_LENGTH] + "\\n[Truncated]"
        
        print(f"💰 API Call - Context: {len(full_context)} chars, Max tokens: {MAX_TOKENS_PER_REQUEST}")
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Cheapest model
            messages=[
                {"role": "system", "content": "Code analyst. Be concise."},
                {"role": "user", "content": f"Context:\\n{full_context}\\n\\nQ: {question}"}
            ],
            max_tokens=MAX_TOKENS_PER_REQUEST,
            temperature=TEMPERATURE
        )
        
        # 🧠 CACHE THE RESPONSE TO SAVE FUTURE API CALLS
        result = response.choices[0].message.content
        response_cache[cache_key] = result
        
        # Track API usage
        track_api_usage(response.usage.total_tokens)
        
        return resultv()

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

# 💰 COST OPTIMIZATION SETTINGS 💰
COST_OPTIMIZED = True
MAX_TOKENS_PER_REQUEST = 600 if COST_OPTIMIZED else 1000
TEMPERATURE = 0.1 if COST_OPTIMIZED else 0.7
MAX_CONTEXT_LENGTH = 4000 if COST_OPTIMIZED else 8000
MAX_FILES_IN_CONTEXT = 2 if COST_OPTIMIZED else 3
MAX_CHARS_PER_FILE = 1000 if COST_OPTIMIZED else 2000

# 🧠 SMART CACHING SYSTEM TO SAVE API COSTS 🧠
response_cache = {}
api_call_count = 0
tokens_used = 0

def get_cache_key(question, context_type, content_hash):
    return f"{question[:100]}_{context_type}_{content_hash[:10]}"

def track_api_usage(tokens):
    global api_call_count, tokens_used
    api_call_count += 1
    tokens_used += tokens
    estimated_cost = tokens_used * 0.000002  # GPT-3.5-turbo pricing
    print(f"💰 API Stats: {api_call_count} calls, {tokens_used} tokens, ~${estimated_cost:.4f}")

# Enhanced storage for multi-language code content
code_analysis = {
    "content": {},
    "structure": {},
    "languages": {},
    "metrics": {},
    "security_issues": [],
    "api_endpoints": [],
    "documentation": "",
    "repository_info": {}
}

# Supported file extensions and languages
SUPPORTED_LANGUAGES = {
    '.py': 'python',
    '.js': 'javascript', 
    '.jsx': 'javascript',
    '.ts': 'typescript',
    '.tsx': 'typescript',
    '.java': 'java',
    '.cpp': 'cpp',
    '.c': 'c',
    '.h': 'c',
    '.hpp': 'cpp',
    '.go': 'go',
    '.rs': 'rust',
    '.php': 'php',
    '.rb': 'ruby',
    '.swift': 'swift',
    '.kt': 'kotlin',
    '.cs': 'csharp',
    '.html': 'html',
    '.css': 'css',
    '.sql': 'sql',
    '.json': 'json',
    '.xml': 'xml',
    '.yaml': 'yaml',
    '.yml': 'yaml'
}

def clone_and_analyze_repo(repo_url):
    """Enhanced repository analysis with multi-language support"""
    global code_analysis
    
    # Reset analysis
    code_analysis = {
        "content": {},
        "structure": {},
        "languages": {},
        "metrics": {},
        "security_issues": [],
        "api_endpoints": [],
        "documentation": "",
        "repository_info": {}
    }
    
    temp_dir = tempfile.mkdtemp()
    repo_path = os.path.join(temp_dir, "repo")
    
    try:
        # Clone repository
        repo = Repo.clone_from(repo_url, repo_path)
        
        # Get repository info
        code_analysis["repository_info"] = {
            "url": repo_url,
            "name": repo_url.split('/')[-1],
            "clone_time": datetime.now().isoformat(),
            "branches": [str(branch) for branch in repo.branches],
            "total_commits": len(list(repo.iter_commits())),
            "last_commit": str(repo.head.commit.hexsha[:8]) if repo.head.commit else "N/A"
        }
        
        # Analyze all supported files
        file_count = 0
        language_stats = defaultdict(int)
        
        for root, dirs, files in os.walk(repo_path):
            # Skip common ignored directories
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', '.vscode', '.idea']]
            
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, repo_path)
                file_ext = os.path.splitext(file)[1].lower()
                
                if file_ext in SUPPORTED_LANGUAGES:
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                        language = SUPPORTED_LANGUAGES[file_ext]
                        language_stats[language] += 1
                        
                        code_analysis["content"][relative_path] = {
                            "content": content,
                            "language": language,
                            "size": len(content),
                            "lines": len(content.split('\n'))
                        }
                        
                        # Analyze specific file types
                        if language == 'python':
                            analyze_python_file(content, relative_path)
                        elif language in ['javascript', 'typescript']:
                            analyze_js_file(content, relative_path)
                        
                        file_count += 1
                        
                    except Exception as e:
                        print(f"Error reading {relative_path}: {str(e)}")
        
        code_analysis["languages"] = dict(language_stats)
        code_analysis["metrics"]["total_files"] = file_count
        code_analysis["metrics"]["total_lines"] = sum(file_info["lines"] for file_info in code_analysis["content"].values())
        
        # Generate project structure
        generate_project_structure(repo_path)
        
        # Perform security analysis
        perform_security_analysis()
        
        # Generate documentation
        generate_auto_documentation()
        
        return True, f"✅ Successfully analyzed {file_count} files in {len(language_stats)} languages"
        
    except Exception as e:
        return False, f"❌ Error analyzing repository: {str(e)}"
    finally:
        try:
            shutil.rmtree(temp_dir)
        except:
            pass

def analyze_python_file(content, file_path):
    """Analyze Python file for functions, classes, and API endpoints"""
    try:
        tree = ast.parse(content)
        
        functions = []
        classes = []
        imports = []
        api_endpoints = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append({
                    "name": node.name,
                    "line": node.lineno,
                    "args": [arg.arg for arg in node.args.args],
                    "decorators": [d.id if hasattr(d, 'id') else str(d) for d in node.decorator_list]
                })
                
                # Check for Flask routes
                for decorator in node.decorator_list:
                    if hasattr(decorator, 'attr') and decorator.attr == 'route':
                        if hasattr(decorator, 'args') and decorator.args:
                            route = decorator.args[0].s if hasattr(decorator.args[0], 's') else str(decorator.args[0])
                            api_endpoints.append({
                                "path": route,
                                "method": "GET",  # Default
                                "function": node.name,
                                "file": file_path
                            })
            
            elif isinstance(node, ast.ClassDef):
                classes.append({
                    "name": node.name,
                    "line": node.lineno,
                    "methods": [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                })
            
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        
        code_analysis["structure"][file_path] = {
            "functions": functions,
            "classes": classes,
            "imports": imports
        }
        
        code_analysis["api_endpoints"].extend(api_endpoints)
        
    except Exception as e:
        print(f"Error analyzing Python file {file_path}: {str(e)}")

def analyze_js_file(content, file_path):
    """Basic JavaScript/TypeScript analysis"""
    # Simple regex-based analysis for JS/TS files
    functions = re.findall(r'function\s+(\w+)', content)
    classes = re.findall(r'class\s+(\w+)', content)
    imports = re.findall(r'import.*from\s+[\'"]([^\'"]+)[\'"]', content)
    
    # Check for API endpoints (Express.js style)
    api_routes = re.findall(r'app\.(get|post|put|delete)\([\'"]([^\'"]+)[\'"]', content)
    
    for method, route in api_routes:
        code_analysis["api_endpoints"].append({
            "path": route,
            "method": method.upper(),
            "file": file_path
        })
    
    code_analysis["structure"][file_path] = {
        "functions": [{"name": f} for f in functions],
        "classes": [{"name": c} for c in classes],
        "imports": imports
    }

def generate_project_structure(repo_path):
    """Generate hierarchical project structure"""
    structure = {}
    
    for root, dirs, files in os.walk(repo_path):
        # Skip ignored directories
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', '.vscode', '.idea']]
        
        relative_root = os.path.relpath(root, repo_path)
        if relative_root == '.':
            relative_root = ''
        
        current_level = structure
        if relative_root:
            for part in relative_root.split(os.sep):
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]
        
        for file in files:
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in SUPPORTED_LANGUAGES or file in ['README.md', 'package.json', 'requirements.txt']:
                current_level[file] = {
                    "type": "file",
                    "language": SUPPORTED_LANGUAGES.get(file_ext, "text")
                }
    
    code_analysis["structure"]["project_tree"] = structure

def perform_security_analysis():
    """Perform basic security analysis"""
    security_issues = []
    
    for file_path, file_info in code_analysis["content"].items():
        content = file_info["content"]
        language = file_info["language"]
        
        # Common security patterns
        security_patterns = {
            "hardcoded_password": r'password\s*=\s*["\'][^"\']+["\']',
            "sql_injection": r'(SELECT|INSERT|UPDATE|DELETE).*\+.*\+',
            "xss_vulnerability": r'innerHTML\s*=.*\+',
            "api_key_exposure": r'(api_key|secret_key|access_token)\s*=\s*["\'][^"\']+["\']',
            "unsafe_eval": r'eval\s*\(',
            "debug_mode": r'debug\s*=\s*True'
        }
        
        for issue_type, pattern in security_patterns.items():
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                line_number = content[:match.start()].count('\n') + 1
                security_issues.append({
                    "type": issue_type,
                    "file": file_path,
                    "line": line_number,
                    "severity": "high" if issue_type in ["sql_injection", "xss_vulnerability"] else "medium",
                    "description": f"Potential {issue_type.replace('_', ' ')} found"
                })
    
    code_analysis["security_issues"] = security_issues

def generate_auto_documentation():
    """Generate automatic documentation"""
    repo_info = code_analysis["repository_info"]
    languages = code_analysis["languages"]
    metrics = code_analysis["metrics"]
    
    doc_sections = []
    
    # Project overview
    doc_sections.append(f"# {repo_info.get('name', 'Project')} Documentation")
    doc_sections.append(f"\n## Project Overview")
    doc_sections.append(f"- **Repository**: {repo_info.get('url', 'N/A')}")
    doc_sections.append(f"- **Total Files**: {metrics.get('total_files', 0)}")
    doc_sections.append(f"- **Total Lines**: {metrics.get('total_lines', 0)}")
    doc_sections.append(f"- **Languages**: {', '.join(languages.keys())}")
    
    # Language breakdown
    if languages:
        doc_sections.append(f"\n## Language Distribution")
        for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
            doc_sections.append(f"- **{lang.title()}**: {count} files")
    
    # API endpoints
    if code_analysis["api_endpoints"]:
        doc_sections.append(f"\n## API Endpoints")
        for endpoint in code_analysis["api_endpoints"]:
            doc_sections.append(f"- **{endpoint['method']}** `{endpoint['path']}` - {endpoint.get('function', 'N/A')}")
    
    # Security summary
    if code_analysis["security_issues"]:
        high_issues = [i for i in code_analysis["security_issues"] if i["severity"] == "high"]
        medium_issues = [i for i in code_analysis["security_issues"] if i["severity"] == "medium"]
        doc_sections.append(f"\n## Security Analysis")
        doc_sections.append(f"- **High Priority Issues**: {len(high_issues)}")
        doc_sections.append(f"- **Medium Priority Issues**: {len(medium_issues)}")
    
    code_analysis["documentation"] = "\n".join(doc_sections)

def ask_openai_enhanced(question, context_type="general"):
    """💰 COST-OPTIMIZED AI responses with smart caching"""
    try:
        # 🧠 CHECK CACHE FIRST TO SAVE API CALLS
        content_hash = str(hash(str(code_analysis.get("content", {}))))
        cache_key = get_cache_key(question, context_type, content_hash)
        
        if cache_key in response_cache:
            print("💰 Using cached response - NO API COST!")
            return response_cache[cache_key]
        
        # Prepare context based on type (OPTIMIZED)
        context_parts = []
        
        if context_type == "security":
            context_parts.append(f"Security Issues: {len(code_analysis['security_issues'])}")
            if code_analysis["security_issues"]:
                for issue in code_analysis["security_issues"][:3]:  # Reduced to 3
                    context_parts.append(f"- {issue['type']} in {issue['file']}")
        
        elif context_type == "api":
            if code_analysis["api_endpoints"]:
                context_parts.append("APIs:")
                for endpoint in code_analysis["api_endpoints"][:5]:  # Limit to 5
                    context_parts.append(f"- {endpoint['method']} {endpoint['path']}")
        
        elif context_type == "structure":
            context_parts.append(f"Languages: {', '.join(list(code_analysis['languages'].keys())[:5])}")
            context_parts.append(f"Files: {code_analysis['metrics'].get('total_files', 0)}")
        
        # Add code content (HEAVILY OPTIMIZED)
        code_content = ""
        for file_path, file_info in list(code_analysis["content"].items())[:MAX_FILES_IN_CONTEXT]:
            code_content += f"\\n=== {file_path} ===\\n"
            code_content += file_info["content"][:MAX_CHARS_PER_FILE]
            if len(file_info["content"]) > MAX_CHARS_PER_FILE:
                code_content += "\n[Truncated...]"
        
        full_context = "\n".join(context_parts) + code_content
        
        # Truncate if too long (reduced for cost efficiency)
        if len(full_context) > 4000:
            full_context = full_context[:4000] + "\n\n[Context truncated]"
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a code analyst. Be concise and focus on key insights."},
                {"role": "user", "content": f"Context:\n{full_context}\n\nQ: {question}"}
            ],
            max_tokens=600,
            temperature=0.1
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error getting AI response: {str(e)}"

def execute_code_safely(code, language="python"):
    """Safely execute code in sandbox"""
    if language != "python":
        return "Code execution currently only supported for Python"
    
    try:
        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        # Execute code with restrictions
        allowed_builtins = {
            'print': print,
            'len': len,
            'str': str,
            'int': int,
            'float': float,
            'list': list,
            'dict': dict,
            'range': range,
            'enumerate': enumerate,
            'zip': zip
        }
        
        exec(code, {"__builtins__": allowed_builtins})
        
        # Get output
        output = captured_output.getvalue()
        sys.stdout = old_stdout
        
        return output if output else "Code executed successfully (no output)"
        
    except Exception as e:
        sys.stdout = old_stdout
        return f"Execution error: {str(e)}"

# Routes
@app.route('/')
def index():
    return render_template('enhanced_index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/playground')
def playground():
    return render_template('playground.html')

@app.route('/api-explorer')
def api_explorer():
    return render_template('api_explorer.html')

@app.route('/chatbot', methods=["POST"])
def gitRepo():
    user_input = request.form['question']
    
    if user_input.strip():
        success, message = clone_and_analyze_repo(user_input)
        return jsonify({"response": message})
    else:
        return jsonify({"response": "Please provide a valid GitHub repository URL."})

@app.route("/get", methods=["POST"])
def chat():
    msg = request.form["msg"]
    
    if msg.lower() == "clear":
        global code_analysis
        code_analysis = {"content": {}, "structure": {}, "languages": {}, "metrics": {}, "security_issues": [], "api_endpoints": [], "documentation": "", "repository_info": {}}
        return "🗑️ Analysis data cleared."
    
    if not code_analysis["content"]:
        return "📝 Please first load a repository using the form above."
    
    # Determine context type based on question
    context_type = "general"
    if any(word in msg.lower() for word in ["security", "vulnerability", "secure"]):
        context_type = "security"
    elif any(word in msg.lower() for word in ["api", "endpoint", "route"]):
        context_type = "api"
    elif any(word in msg.lower() for word in ["structure", "architecture", "organization"]):
        context_type = "structure"
    
    response = ask_openai_enhanced(msg, context_type)
    return response

@app.route('/api/project-info')
def get_project_info():
    return jsonify(code_analysis)

@app.route('/api/code-structure')
def get_code_structure():
    return jsonify(code_analysis["structure"])

@app.route('/api/security-analysis')
def get_security_analysis():
    return jsonify(code_analysis["security_issues"])

@app.route('/api/documentation')
def get_documentation():
    return jsonify({"documentation": code_analysis["documentation"]})

@app.route('/api/execute-code', methods=['POST'])
def execute_code():
    data = request.get_json()
    code = data.get('code', '')
    language = data.get('language', 'python')
    
    result = execute_code_safely(code, language)
    return jsonify({"result": result})

@app.route('/api/generate-readme')
def generate_readme():
    if not code_analysis["content"]:
        return jsonify({"error": "No repository loaded"})
    
    try:
        prompt = f"""Generate a professional README.md for this project:
        
        Project Info: {code_analysis['repository_info']}
        Languages: {code_analysis['languages']}
        API Endpoints: {code_analysis['api_endpoints']}
        
        Include sections for: Description, Installation, Usage, API Documentation, Contributing"""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a technical writer. Generate professional README.md content."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500
        )
        
        readme_content = response.choices[0].message.content
        return jsonify({"readme": readme_content})
        
    except Exception as e:
        return jsonify({"error": str(e)})

# 💰 NEW ROUTE: API COST TRACKING
@app.route('/api/cost-stats')
def get_cost_stats():
    estimated_cost = tokens_used * 0.000002  # GPT-3.5-turbo pricing
    return jsonify({
        "api_calls": api_call_count,
        "tokens_used": tokens_used,
        "estimated_cost_usd": round(estimated_cost, 6),
        "cache_hits": len(response_cache),
        "cost_optimized": COST_OPTIMIZED
    })

if __name__ == '__main__':
    print("🚀 Starting Enhanced Source Code Analysis AI...")
    print("📱 Features: Multi-language support, Security analysis, Code playground, API explorer")
    print("📱 Open your browser and go to: http://localhost:8080")
    app.run(host="0.0.0.0", port=8080, debug=True)