import subprocess
from utils.port_utils import get_free_port
import os
def auto_fix(error,service_path):
    error=error.lower()

    if "no module named" in error or "module not found" in error:
        req_path = os.path.join(service_path, "requirements.txt")

        if os.path.exists(req_path):
            print("Auto-fix: Installing Python dependencies...\n")
            subprocess.run("pip install -r requirements.txt", shell=True, cwd=service_path)
            return True

    if "npm" in error and "not found" in error:
        print("Auto-fix: npm not found. Please install Node.js.")
        return False
    if "address already in use" in error:
        print("Auto-fix: Port conflict detected.\n")
        return "port"

    if "node_modules" in error or "cannot find module" in error:
        print("Auto-fix: Installing node dependencies...\n")
        subprocess.run("npm install", shell=True, cwd=service_path)
        return True
    return False
def handle_port_conflict(service):
    new_port = get_free_port()
    print(f"Auto-fix: Switching to free port {new_port}")

    command = service["command"]

    if "uvicorn" in command:
        command += f" --port {new_port}"

    elif "npm start" in command or "npm run dev" in command:
        command = f"set PORT={new_port} && {command}"

    service["command"] = command
    return service
def extract_code(ai_response):
    lines = ai_response.split("\n")import subprocess
import os
from utils.port_utils import get_free_port


def auto_fix(error, service_path):
    error = error.lower()

    
    if "no module named" in error or "module not found" in error:
        req_path = os.path.join(service_path, "requirements.txt")

        if os.path.exists(req_path):
            print("Auto-fix: Installing Python dependencies...\n")
            subprocess.run(
                "pip install -r requirements.txt",
                shell=True,
                cwd=service_path
            )
            return True


    if "npm" in error and "not found" in error:
        print("Auto-fix: npm not found. Please install Node.js.")
        return False

    
    if "node_modules" in error or "cannot find module" in error:
        print("Auto-fix: Installing node dependencies...\n")
        subprocess.run("npm install", shell=True, cwd=service_path)
        return True


    if "address already in use" in error:
        print("Auto-fix: Port conflict detected.\n")
        return "port"

    return False


def handle_port_conflict(service):
    new_port = get_free_port()
    print(f"Auto-fix: Switching to free port {new_port}")

    command = service["command"]

    if "uvicorn" in command:
        command += f" --port {new_port}"

    elif "npm start" in command or "npm run dev" in command:
        command = f"set PORT={new_port} && {command}"

    service["command"] = command
    return service

def extract_code(ai_response):
    """
    Extracts CODE section from AI response
    """
    lines = ai_response.split("\n")
    code_lines = []
    capture = False

    for line in lines:
        if line.strip().startswith("CODE:"):
            capture = True
            continue
        if capture:
            code_lines.append(line)

    return "\n".join(code_lines).strip()


def apply_ai_fix(service, ai_response):
    """
    Applies fix suggested by AI
    Supports:
    - Command fixes
    - Code fixes
    """
    code = extract_code(ai_response)

    if not code:
        print("AI Fix: No usable code found.")
        return False

    print("\nApplying AI Fix...\n")

    try:
        
        if is_command(code):
            print(f"Running command: {code}\n")

            subprocess.run(
                code,
                shell=True,
                cwd=service["path"]
            )
            return True

    
        entry = service.get("entry")

        if entry:
            file_path = os.path.join(service["path"], entry)

            print(f"Updating file: {file_path}\n")

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)

            return True

        print("AI Fix: No entry file found.")
        return False

    except Exception as e:
        print(f"AI Fix Error: {e}")
        return False

def is_command(text):
    """
    Detect if AI output is a command
    """
    keywords = ["pip", "npm", "yarn", "python", "node", "uvicorn", "go", "cargo"]

    return any(text.strip().startswith(k) for k in keywords)
    code_lines = []
    capture = False

    for line in lines:
        if line.strip().startswith("CODE:"):
            capture = True
            continue
        if capture:
            code_lines.append(line)

    return "\n".join(code_lines).strip()