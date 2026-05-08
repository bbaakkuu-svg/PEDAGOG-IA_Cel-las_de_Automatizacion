import os
from typing import List
from rich.table import Table
from rich.console import Console
from .strategies import SyncStrategy

console = Console()

class SyncOrchestrator:
    """
    Orquestador de Estado Global:
    Detecta activos y aplica la estrategia de sincronización inyectada.
    """
    
    def __init__(self, strategy: SyncStrategy):
        self.strategy = strategy
        self.projects = [
            "auto_repo_scaffolder",
            "api_intelligence_wrapper",
            "cloud_native_task_scheduler",
            "ecosystem_sync_orchestrator"
        ]

    def sync_all(self):
        table = Table(title="Estado de Sincronización del Ecosistema")
        table.add_column("Proyecto", style="cyan")
        table.add_column("Estrategia", style="magenta")
        table.add_column("Estado", style="green")

        for project in self.projects:
            success = self.strategy.sync_project(project, f"Sync: Update {project} to latest cell standards")
            status = "[bold green]SYNCED[/bold green]" if success else "[bold red]FAILED[/bold red]"
            table.add_row(project, self.strategy.name, status)

        console.print(table)
