import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def ask_ai(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0,
                            "num_predict":300
                            },
            },
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        return data.get("response", "").strip()

    except requests.exceptions.ConnectionError:
        return "Error: Ollama is not running."

    except requests.exceptions.Timeout:
        return "Error: Request timed out."

    except Exception as e:
        return f"AI Error: {str(e)}"
