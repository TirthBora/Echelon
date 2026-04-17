def get_command(service):
    lang = service.get("language")
    entry = service.get("entry")

    if lang == "python":
        if entry:
            return f"python {entry}"
        return "python main.py"

    if lang == "node":
        return "npm install && npm start"

    if lang == "java":
        return "mvn spring-boot:run || gradle run"

    if lang == "go":
        if entry:
            return f"go run {entry}"
        return "go run ."

    if lang == "rust":
        return "cargo run"

    if lang == "cpp":
        return "g++ *.cpp -o app && ./app"

    return None