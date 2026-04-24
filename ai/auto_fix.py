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