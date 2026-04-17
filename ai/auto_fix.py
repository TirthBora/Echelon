import subprocess
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

    if "node_modules" in error or "cannot find module" in error:
        print("Auto-fix: Installing node dependencies...\n")
        subprocess.run("npm install", shell=True, cwd=service_path)
        return True

    if "address already in use" in error:
        print("Auto-fix: Port conflict detected. Try another port manually.")
        return False

    return False
