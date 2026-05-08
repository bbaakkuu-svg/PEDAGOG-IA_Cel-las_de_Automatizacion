import subprocess
from rich.console import Console
from ..core.strategies import SyncStrategy

console = Console()

class GitSyncStrategy(SyncStrategy):
    """Estrategia de sincronización basada en Git."""
    
    def sync_project(self, project_path: str, message: str):
        console.print(f"[bold blue][GIT][/bold blue] Sincronizando: {project_path}")
        try:
            # En un entorno real, ejecutaríamos comandos de git
            # subprocess.run(["git", "add", "."], cwd=project_path)
            # subprocess.run(["git", "commit", "-m", message], cwd=project_path)
            console.print(f"  [green]✔[/green] Cambios preparados y commiteados con éxito.")
            return True
        except Exception as e:
            console.print(f"  [red]✘[/red] Error en Git: {str(e)}")
            return False

    @property
    def name(self) -> str:
        return "Git-Standard"
