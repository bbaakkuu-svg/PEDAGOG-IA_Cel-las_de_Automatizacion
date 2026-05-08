from rich.console import Console
from ..core.interfaces import TaskExecutor

console = Console()

class LocalExecutor(TaskExecutor):
    """Implementación para ejecución en servidor local."""
    
    def run(self, task_name: str, payload: dict):
        console.print(f"[bold blue][LOCAL][/bold blue] Ejecutando tarea: {task_name}...")
        # Lógica de simulación local
        return {"status": "success", "engine": self.environment}

    @property
    def environment(self) -> str:
        return "Local-Workstation"

class CloudExecutor(TaskExecutor):
    """Implementación (Mock) para ejecución en Cloud Functions/Lambda."""
    
    def run(self, task_name: str, payload: dict):
        console.print(f"[bold magenta][CLOUD][/bold magenta] Desplegando tarea {task_name} a la nube...")
        # Simulación de llamada a API Cloud
        return {"status": "dispatched", "engine": self.environment}

    @property
    def environment(self) -> str:
        return "AWS-Lambda-Runtime"
