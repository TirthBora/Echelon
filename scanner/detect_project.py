import os


def detect_project(path="."):
    services = []

    for root, dirs, files in os.walk(path):

        service = {"path": root, "language": None, "framework": None, "entry": None}

        files_set = set(files)

        if any(f.endswith(".py") for f in files):
            service["language"] = "python"

        elif any(f.endswith(".js") or f.endswith(".ts") for f in files):
            service["language"] = "node"

        elif any(f.endswith(".java") for f in files):
            service["language"] = "java"

        elif any(f.endswith(".cpp") or f.endswith(".c") for f in files):
            service["language"] = "cpp"

        elif any(f.endswith(".go") for f in files):
            service["language"] = "go"

        elif any(f.endswith(".rs") for f in files):
            service["language"] = "rust"

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

        for f in files:
            if f.lower() in ["main.py", "app.py", "server.py", "index.js", "main.go"]:
                service["entry"] = f
                break

        if service["language"]:
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
