from typing import Optional
import clipboard
import sys
import os
from rich.console import Console
from src.app.git_handler import get_git_diff
from src.app.llm_client import verify_changes
from src.app.config import LLM_PROMPT


def main(repository_path: Optional[str]):
    """Executa o SmartCommit e copia a mensagem de commit gerada para a área de transferência."""
    if repository_path is None or not os.path.isdir(repository_path):
        print("Usage: python main.py <repository_path>")
        print(f"Invalid path: {repository_path}")
        return

    print(f"Repository path: {repository_path}")
    print(f"Prompt: {LLM_PROMPT}")

    git_changes = get_git_diff(repository_path)
    commit_message = verify_changes(git_changes)
    
    clipboard.copy(commit_message)

    console = Console()
    console.print("Result copied to clipboard:")
    console.print(commit_message)


if __name__ == "__main__":
    repository_path = sys.argv[1] if len(sys.argv) > 1 else None
    main(repository_path)
