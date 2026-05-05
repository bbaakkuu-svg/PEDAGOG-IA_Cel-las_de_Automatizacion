import sys
from pathlib import Path
from rich.console import Console
from .core.models import RepoConfig
from .core.scaffolder import RepoScaffolder, FileSystemAdapter

console = Console()

def main():
    console.print("[bold blue]Antigravity Scaffolder[/bold blue] - Generando base de Arquitectura Limpia...")
    
    # Simulación de entrada (En una versión final usaría argparse o Typer)
    try:
        config = RepoConfig(
            project_name="nuevo_modulo_automatizacion",
            description="Automatización de alto nivel para procesos internos de Docensas."
        )
        
        scaffolder = RepoScaffolder(FileSystemAdapter())
        scaffolder.execute(config, Path.cwd())
        
        console.print(f"[bold green]✔ Éxito:[/bold green] Repositorio '{config.project_name}' creado satisfactoriamente.")
        
    except Exception as e:
        console.print(f"[bold red]✘ Error:[/bold red] {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
