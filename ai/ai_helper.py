def build_error_prompt(error, service):
    return f"""
        You are a strict coding assistant.

        Return ONLY in this format:

        ERROR:
        <short explanation>

        FIX:
        <what to change>

        CODE:
        <corrected code OR exact command>

        ---

        Error:
        {error}

        Project:
        Language: {service.get("language")}
        Path: {service.get("path")}
        """
