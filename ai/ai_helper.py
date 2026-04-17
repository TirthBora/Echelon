def build_error_prompt(error, service):
    return f"""
I ran a project and got this error:

{error}

Project details:
- Language: {service.get("language")}
- Framework: {service.get("framework")}
- Path: {service.get("path")}

Explain:
1. What the error means
2. How to fix it
3. Exact command if possible
"""