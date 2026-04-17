def suggest_fix(eror):
    error=error.lower()
    if "module not found" in error or "no module named" in error:
        print("Suggestion: Run 'pip install -r requirements.txt'")

    elif "address already in use" in error or "port" in error:
        print("Suggestion: Try running on a different port")

    elif "npm not found" in error:
        print("Suggestion: Install Node.js and npm")

    elif "permission denied" in error:
        print("Suggestion: Try running with proper permissions")

    else:
        print("Suggestion: Check dependencies or configuration")