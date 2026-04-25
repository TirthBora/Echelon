import os
from ai.ai_engine import ask_ai


def get_key_files(path):
    important = [
        "package.json", "main.py", "app.py",
        "server.js", "manage.py", "pom.xml"
    ]

    data = ""
    for f in important:
        fp = os.path.join(path, f)
        if os.path.exists(fp):
            try:
                with open(fp, "r", encoding="utf-8") as file:
                    data += f"\n--- {f} ---\n"
                    data += file.read()[:1000]
            except:
                pass
    return data


def ask_ai_for_command(service):
    files = os.listdir(service["path"])
    code = get_key_files(service["path"])

    prompt = f"""
You are an expert software engineer.

Project:
Path: {service['path']}
Language: {service['language']}
Files: {files}

Code:
{code}

Detect:
1. Framework
2. Command to run project

Rules:
- React/Vite → npm install && npm run dev
- Next.js → npm install && npm run dev
- Vue → npm install && npm run dev
- Angular → npm install && ng serve
- Express → node server.js
- NestJS → npm run start:dev
- FastAPI → uvicorn main:app --reload
- Flask → python app.py
- Django → python manage.py runserver
- Static → python -m http.server 5500
- Spring Boot → mvn spring-boot:run

Return ONLY:

FRAMEWORK: <name>
COMMAND: <command>
"""

    response = ask_ai(prompt)

    print("\n[AI DETECTION]\n", response)

    framework = None
    command = None

    for line in response.splitlines():
        if "FRAMEWORK:" in line:
            framework = line.split("FRAMEWORK:")[-1].strip().lower()
        if "COMMAND:" in line:
            command = line.split("COMMAND:")[-1].strip()

    if framework:
        service["framework"] = framework

    return command


def get_command(service):
    lang = service.get("language")
    framework = service.get("framework")
    entry = service.get("entry")

    if framework in ["react", "vite"]:
        return "npm install && npm run dev"

    if framework == "nextjs":
        return "npm install && npm run dev"

    if framework == "vue":
        return "npm install && npm run dev"

    if framework == "angular":
        return "npm install && ng serve"

    if framework == "static":
        return "python -m http.server 5500"

    if framework == "fastapi":
        entry = (entry or "main.py").replace(".py", "")
        return f"uvicorn {entry}:app --reload"

    if framework == "flask":
        return f"python {entry or 'app.py'}"

    if framework == "django":
        return "python manage.py runserver"

    if framework == "express":
        return f"node {entry or 'server.js'}"

    if framework == "nestjs":
        return "npm install && npm run start:dev"

    if framework == "spring":
        return "mvn spring-boot:run || gradle bootRun"

    if lang == "python":
        return f"python {entry}" if entry else "python main.py"

    if lang == "node":
        return "npm install && npm start"

    if lang == "java":
        return "mvn spring-boot:run || gradle run"

    if lang == "go":
        return f"go run {entry}" if entry else "go run ."

    if lang == "rust":
        return "cargo run"

    if lang == "cpp":
        return "g++ *.cpp -o app && ./app"

    if lang == "csharp":
        return "dotnet run"

    if lang == "php":
        return "php -S localhost:8000"

    if lang == "ruby":
        return "rails server || ruby app.rb"

    if service.get("needs_ai"):
        return ask_ai_for_command(service)

    return None