import os

IGNORE_DIRS = {
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    ".git",
    "dist",
    "build"
}


def detect_project(path="."):
    services = []

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
    
        files_set = set(files)

        service = {
            "path": root,
            "language": None,
            "framework": None,
            "entry": None
        }
        if root==path:
            service["is_root"]=True

        if "package.json" in files_set:
            service["language"] = "node"

        elif "requirements.txt" in files_set or "pyproject.toml" in files_set:
            service["language"] = "python"


        elif "pom.xml" in files_set or "build.gradle" in files_set:
            service["language"] = "java"

        elif "go.mod" in files_set:
            service["language"] = "go"

        elif "Cargo.toml" in files_set:
            service["language"] = "rust"
    # Fallback detection
        if not service["language"]:
            if any(f.endswith(".py") for f in files):
                service["language"] = "python"
            elif any(f.endswith(".js") for f in files):
                service["language"] = "node"
            elif any(f.endswith(".java") for f in files):
                service["language"] = "java"
            elif any(f.endswith(".cpp") or f.endswith(".c") for f in files):
                service["language"] = "cpp"
            elif any(f.endswith(".go") for f in files):
                service["language"] = "go"
            elif any(f.endswith(".rs") for f in files):
                service["language"] = "rust"

        entry_files = [
            "main.py", "app.py", "server.py",
            "index.js", "server.js",
            "main.go"
        ]

        for f in files:
            if f.lower() in entry_files:
                service["entry"] = f
                break

        if service["language"] and service["entry"]:
            if os.path.abspath(root) == os.path.abspath(path):
                service["is_root"] = True
            services.append(service)

    return services


def classify_service(service):
    framework = service.get("framework")
    lang = service.get("language")

    if framework in ["fastapi", "flask", "django", "express"]:
        return "backend"

    if framework in ["react", "nextjs"]:
        return "frontend"

    if lang == "python":
        return "backend"

    if lang == "node":
        return "frontend"

    return "unknown"