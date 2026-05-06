# main.py - Generador Dinámico de Material (IA)
# -------------------------------------------------------------------------
import os
import sys
import json
import time

# Manejo de dependencias con reporte amigable
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt
    from rich.live import Live
    from rich.spinner import Spinner
except ImportError:
    print("Error: Soporte para 'rich' no disponible. Instale 'rich'.")
    sys.exit(1)

try:
    from core.engine import ContentEngine
except ImportError as e:
    # Intento de resolución para PyInstaller
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    try:
        from core.engine import ContentEngine
    except ImportError:
        print(f"Error crítico: Módulos del núcleo no encontrados. ({e})")
        sys.exit(1)

console = Console()

class MaterialGeneratorSEA:
    def __init__(self):
        self.engine = None
        self._initialize_engine()
        self.output_dir = "output"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _initialize_engine(self):
        try:
            self.engine = ContentEngine()
        except Exception as e:
            console.print(f"[bold red]✘ Error al inicializar el motor de IA:[/bold red] {e}")

    def process_content(self, text: str, filename: str = "entrada_manual"):
        if not self.engine:
            console.print("[bold red]✘ Motor no disponible.[/bold red]")
            return

        with Live(Spinner("dots", text=f"Generando material para: {filename}..."), refresh_per_second=10) as live:
            try:
                # 1. Generar Resumen
                summary = self.engine.generate_summary(text)
                
                # 2. Generar Quiz
                quiz = self.engine.generate_quiz(text)
                
                time.sleep(1) # Simulación de procesamiento
                
                # Guardar resultados
                output_filename = f"material_{int(time.time())}.json"
                output_path = os.path.join(self.output_dir, output_filename)
                
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump({"summary": summary, "quiz": quiz}, f, indent=4, ensure_ascii=False)
                
                live.update(Panel(f"[bold green]✔ Proceso completado exitosamente[/bold green]\n[dim]Archivo: {output_path}[/dim]", border_style="green"))
                
                # Mostrar vista previa
                console.print(Panel(summary, title="[bold blue]Resumen Ejecutivo[/bold blue]", expand=False))
                console.print(f"\n[bold yellow]📝 Cuestionario ({len(quiz)} preguntas):[/bold yellow]")
                for i, q in enumerate(quiz, 1):
                    console.print(f" {i}. [italic]{q['question']}[/italic]")
                
            except Exception as e:
                live.update(Panel(f"[bold red]✘ Error durante la generación:[/bold red]\n{e}", border_style="red"))

    def run_interactive(self):
        console.print(Panel.fit(
            "[bold cyan]PEDAGOG-IA: Generador Dinámico de Material[/bold cyan]\n"
            "[dim]Industrialización v1.0 | Antigravity 2026[/dim]",
            border_style="cyan"
        ))

        while True:
            console.print("\n[bold white]Opciones:[/bold white]")
            console.print(" 1. Arrastrar archivo de texto (.txt)")
            console.print(" 2. Ingresar texto manualmente")
            console.print(" 3. Ejecutar demo")
            console.print(" 4. Salir")
            
            choice = Prompt.ask("\nSeleccione una opción", choices=["1", "2", "3", "4"], default="3")
            
            if choice == "1":
                path = Prompt.ask("Arrastre el archivo aquí y presione Enter").strip('"').strip("'")
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                    self.process_content(content, os.path.basename(path))
                else:
                    console.print("[bold red]Archivo no encontrado.[/bold red]")
            
            elif choice == "2":
                content = Prompt.ask("Ingrese el contenido para procesar")
                if content:
                    self.process_content(content)
            
            elif choice == "3":
                demo_text = "La IA en la educación permite personalizar el aprendizaje mediante células de automatización que generan feedback en tiempo real."
                self.process_content(demo_text, "Demo_Mode")
            
            elif choice == "4":
                console.print("[yellow]Saliendo...[/yellow]")
                break

if __name__ == "__main__":
    app = MaterialGeneratorSEA()
    if len(sys.argv) > 1:
        # Modo directo si se arrastra un archivo al .exe
        path = sys.argv[1]
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                app.process_content(f.read(), os.path.basename(path))
            input("\nPresione Enter para salir...")
    else:
        app.run_interactive()
