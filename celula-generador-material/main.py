# main.py - Generador Dinamico de Material (IA)
# -------------------------------------------------------------------------
from core.engine import ContentEngine
import rich
from rich.console import Console
from rich.panel import Panel
import json
import os

console = Console()

def run_generator():
    console.print("[bold green]📚 Iniciando Generador Dinamico de Material (IA)...[/bold green]")
    
    source_text = "La arquitectura de PEDAGOG-IA se basa en celulas de automatizacion modulares e independientes."
    
    try:
        engine = ContentEngine()
        
        # 1. Generar Resumen
        summary = engine.generate_summary(source_text)
        console.print(Panel(summary, title="[bold blue]Resumen Ejecutivo[/bold blue]", expand=False))
        
        # 2. Generar Quiz
        quiz = engine.generate_quiz(source_text)
        console.print("\n[bold yellow]📝 Cuestionario Generado:[/bold yellow]")
        for i, q in enumerate(quiz, 1):
            console.print(f"{i}. {q['question']}")
            for opt in q['options']:
                console.print(f"   - {opt}")
        
        # Guardar resultados
        output_path = os.path.join("output", "material_generado.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump({"summary": summary, "quiz": quiz}, f, indent=4, ensure_ascii=False)
        
        console.print(f"\n[cyan]✅ Material guardado en: {output_path}[/cyan]")
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")

if __name__ == "__main__":
    run_generator()
