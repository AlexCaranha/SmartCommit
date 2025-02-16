import clipboard
import os
import sys
import json
import subprocess
import requests
from typing import Optional
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.console import Console
from dotenv import load_dotenv

current_directory = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(current_directory, ".env")

load_dotenv(dotenv_path)

LLM_URL: str = os.getenv("LLM_URL", "")
LLM_PROMPT: str = os.getenv("PROMPT_LLM", "")
TEMPERATURE: float = float(os.getenv("TEMPERATURE", 0.7))
MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", -1))


def remove_double_spaces(text) -> str:
    while "  " in text:
        text = text.replace("  ", " ")

    return text


def verify_changes(git_changes: str) -> str:
    if git_changes is None or git_changes == "":
        return "No changes detected from staged (git)."

    payload = json.dumps(
        {
            "messages": [
                {"role": "system", "content": LLM_PROMPT},
                {"role": "user", "content": git_changes},
            ],
            "temperature": TEMPERATURE,
            "max_tokens": MAX_TOKENS,
            "stream": False,
        }
    )
    headers = {"Content-Type": "application/json"}
    response = requests.request("POST", LLM_URL, headers=headers, data=payload)

    response_dict = json.loads(response.text)
    texto_resposta = str(response_dict["choices"][0]["message"]["content"])

    return texto_resposta


def get_changes_from_git() -> str:
    result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)

    if result.returncode != 0:
        return "Erro ao executar o comando git diff: " + result.stderr

    return result.stdout


def get_git_diff(directory) -> str:
    """
    Obtém a diferença (diff) dos arquivos no diretório especificado desde o último commit.
    """
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    )

    try:
        with progress:
            task = progress.add_task(description="Processing ...", total=None)
            os.chdir(directory)

            progress.update(task)
            git_changes = get_changes_from_git()

            progress.update(task)
            git_changes = remove_double_spaces(git_changes)

            progress.update(task)
            text = verify_changes(git_changes)

            return text

    except Exception as e:
        return f"Error: {e}"


def main(repository_path: Optional[str]):
    if LLM_PROMPT == "":
        print("prompt doesn't exist in .env file.")
        return

    if repository_path is None or not os.path.isdir(repository_path):
        print("python script.py <repository_path>")
        print(f"The path '{repository_path}' is not valid.")
        return

    print(f"repository_path: {repository_path}")
    print(f"prompt: {LLM_PROMPT}")

    git_message = get_git_diff(repository_path)
    clipboard.copy(git_message)

    console = Console()
    console.print("Result copied to clipboard:")
    console.print(git_message)


if __name__ == "__main__":
    repository_path: Optional[str] = None if len(sys.argv) < 2 else sys.argv[1]
    main(repository_path)
