import os
import requests

API_KEY = os.getenv("OPENAI_API_KEY")
def ask_ai(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "gpt-4.1-mini",   
            "messages": [
                {"role": "system", "content": "You are a helpful developer assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data
        )

        result = response.json()


        if "error" in result:
            return f"API Error: {result['error']['message']}"

        if "choices" not in result:
            return f"Unexpected API response: {result}"

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"AI Error: {e}"