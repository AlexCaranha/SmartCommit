import json
import requests
from .config import LLM_URL, LLM_PROMPT, TEMPERATURE, MAX_TOKENS

def verify_changes(git_changes: str) -> str:
    """Envia mudanças para o LLM e recebe uma sugestão de commit message."""
    if not git_changes:
        return "No changes detected from staged (git)."

    payload = json.dumps({
        "messages": [
            {"role": "system", "content": LLM_PROMPT},
            {"role": "user", "content": git_changes},
        ],
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "stream": False,
    })

    headers = {"Content-Type": "application/json"}
    response = requests.post(LLM_URL, headers=headers, data=payload)

    try:
        response_dict = response.json()
        return str(response_dict["choices"][0]["message"]["content"])
    except (KeyError, json.JSONDecodeError):
        return "Error processing response from LLM."
