import subprocess

def ask_ai(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3"],
            input=prompt,
            text=True,
            capture_output=True,
            encoding="utf-8"
        )

        output = result.stdout.strip()
        lines = [line.strip() for line in output.split("\n") if line.strip()]

        return lines[-1] if lines else ""

    except Exception as e:
        return f"Ollama Error: {e}"