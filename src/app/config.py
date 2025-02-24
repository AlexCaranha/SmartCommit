LLM_URL = "http://localhost:1234/v1/chat/completions"
LLM_PROMPT = (
    "As a commit message expert, analyze the changes in the source code and suggest a commit "
    "message that is clear, direct, concise, and in English. Highlight instances of new or deleted files. "
    "Provide only the commit message without additional explanations or information. Keep the message brief."
)
TEMPERATURE = 0.7
MAX_TOKENS = -1
