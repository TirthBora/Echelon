import os
import json

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
            "entry": None,
            "needs_ai": False
        }

        if root == path:
            service["is_root"] = True

        if "package.json" in files_set:
            service["language"] = "node"

            try:
                with open(os.path.join(root, "package.json"), "r", encoding="utf-8") as f:
                    data = json.load(f)

                    deps = {
                        **data.get("dependencies", {}),
                        **data.get("devDependencies", {})
                    }

                    if "react" in deps:
                        service["framework"] = "react"
                    elif "next" in deps:
                        service["framework"] = "nextjs"

            except:
                pass

        elif "requirements.txt" in files_set or "pyproject.toml" in files_set:
            service["language"] = "python"

        elif any(f.endswith(".html") for f in files) and not any(f.endswith(".py") for f in files):
            service["language"] = "frontend"
            service["framework"] = "static"

            if "index.html" in files:
                service["entry"] = "index.html"
            else:
                service["entry"] = next((f for f in files if f.endswith(".html")), None)

        if not service["language"]:
            if any(f.endswith(".py") for f in files):
                service["language"] = "python"
            elif any(f.endswith(".js") for f in files):
                service["language"] = "node"

        if service["language"] == "python":
            for file in files:
                if file.endswith(".py"):
                    try:
                        with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                            content = f.read().lower()

                            if "fastapi" in content:
                                service["framework"] = "fastapi"
                                service["entry"] = file
                                break

                            elif "flask" in content:
                                service["framework"] = "flask"
                                service["entry"] = file
                                break

                    except:
                        pass

        if not service["entry"]:
            entry_files = [
                "main.py", "app.py", "server.py",
                "index.js", "server.js"
            ]

            for f in files:
                if f.lower() in entry_files:
                    service["entry"] = f
                    break

        if service["language"] and not service["framework"]:
            service["needs_ai"] = True

        if service["language"]:
            services.append(service)

    return services


def classify_service(service):
    framework = service.get("framework")
    lang = service.get("language")

    if framework in ["fastapi", "flask", "django", "express"]:
        return "backend"

    if framework in ["react", "nextjs", "static"]:
        return "frontend"

    if lang == "python":
        return "backend"

    if lang in ["node", "frontend"]:
        return "frontend"

    return "unknown"