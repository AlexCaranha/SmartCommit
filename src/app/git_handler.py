import subprocess
import os
from rich.progress import Progress, SpinnerColumn, TextColumn
from .utils import remove_double_spaces

def get_changes_from_git() -> str:
    """Obtém as mudanças no Git (staged)."""
    result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
    if result.returncode != 0:
        return f"Erro ao executar git diff: {result.stderr}"
    return result.stdout

def get_git_diff(directory: str) -> str:
    """Obtém o diff dos arquivos do repositório."""
    progress = Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"))

    try:
        with progress:
            task = progress.add_task(description="Processing ...", total=None)
            os.chdir(directory)

            progress.update(task)
            git_changes = get_changes_from_git()
            git_changes = remove_double_spaces(git_changes)

            return git_changes
    except Exception as e:
        return f"Error: {e}"
