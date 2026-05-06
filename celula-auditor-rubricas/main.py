# main.py - Sistema de Evaluación Adaptativo (SEA) v3.0
# -------------------------------------------------------------------------
import sys
import os
import time
import json

# Forzar codificación UTF-8 en Windows para evitar errores con emojis
if sys.platform == "win32":
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except Exception:
        pass

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown

# Intentar importar dependencias locales
try:
    if getattr(sys, 'frozen', False):
        bundle_dir = sys._MEIPASS
        if bundle_dir not in sys.path:
            sys.path.insert(0, bundle_dir)
    
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if root_path not in sys.path:
        sys.path.insert(0, root_path)
    
    try:
        from adapters.pdf_adapter import PDFAdapter
    except ImportError:
        from celula_auditor_rubricas.adapters.pdf_adapter import PDFAdapter
except Exception:
    PDFAdapter = None

console = Console()

class RubricAuditorSEA:
    """Sistema de Evaluación Adaptativo (SEA)"""
    
    def __init__(self):
        self.pdf_adapter = PDFAdapter() if PDFAdapter else None
        # Ruta persistente para la rúbrica activa (en el mismo directorio que el ejecutable/script)
        self.config_path = os.path.join(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__), "active_rubric.json")
        self._show_header()
        
    def _show_header(self):
        rubric_status = "[bold green]Cargada[/bold green]" if os.path.exists(self.config_path) else "[bold red]No definida[/bold red]"
        header = f"""
# 🎓 Sistema de Evaluación Adaptativo (SEA)
*Estado de la Rúbrica:* {rubric_status}

**Instrucciones:**
1. Arrastra un archivo con el nombre 'rubrica' para configurar los criterios.
2. Arrastra los trabajos de los alumnos para evaluarlos con la rúbrica activa.
        """
        console.print(Panel(Markdown(header), border_style="cyan"))

    def process_input(self, file_path):
        if not file_path or not os.path.exists(file_path):
            self._evaluate_demo()
            return

        filename = os.path.basename(file_path).lower()
        
        # Detección: ¿Es una rúbrica o un trabajo?
        if "rubrica" in filename or "criterios" in filename:
            self._ingest_rubric(file_path)
        else:
            self._evaluate_work(file_path)

    def _ingest_rubric(self, path):
        try:
            console.print(f"\n[bold blue]⚙️ Configurando nueva rúbrica desde:[/bold blue] {os.path.basename(path)}")
            text = self.pdf_adapter.extract_text(path) if path.lower().endswith(".pdf") else open(path, 'r', encoding='utf-8').read()
            
            # Extraer criterios (Lógica simple de parseo para la demo)
            # En un entorno real, aquí se usaría la IA para estructurar el JSON de la rúbrica
            rubric_data = {
                "source": os.path.basename(path),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "content": text[:2000], # Limitar para el estado
                "criteria": self._extract_criteria_from_text(text)
            }
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(rubric_data, f, indent=4)
            
            console.print("[bold green]✅ Rúbrica configurada correctamente. Ahora puedes evaluar trabajos.[/bold green]")
        except Exception as e:
            console.print(f"[bold red]Error al cargar la rúbrica:[/bold red] {str(e)}")

    def _extract_criteria_from_text(self, text):
        """Simula la extracción de criterios de un texto de rúbrica."""
        # Si el texto es corto o no tiene saltos, inventamos criterios genéricos
        # En una versión con IA real, esto sería una llamada a Gemini
        lines = [line.strip() for line in text.split('\n') if len(line.strip()) > 10]
        if len(lines) > 3:
            return [lines[i][:50] for i in range(min(3, len(lines)))]
        return ["Calidad Técnica", "Documentación", "Arquitectura"]

    def _evaluate_work(self, path):
        if not os.path.exists(self.config_path):
            console.print("[bold yellow]⚠️ No hay una rúbrica activa. Por favor, carga una primero (archivo con 'rubrica' en el nombre).[/bold yellow]")
            return

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                rubric = json.load(f)

            with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
                progress.add_task(description=f"[bold blue]Evaluando contra rúbrica: {rubric['source']}...[/bold blue]", total=None)
                
                work_text = self.pdf_adapter.extract_text(path) if path.lower().endswith(".pdf") else open(path, 'r', encoding='utf-8').read()
                time.sleep(2)
                
                results = self._perform_comparative_analysis(work_text, rubric)
                self._display_detailed_report(results, os.path.basename(path), rubric['source'])
        
        except Exception as e:
            console.print(f"[bold red]Error en la evaluación:[/bold red] {str(e)}")

    def _perform_comparative_analysis(self, work_text, rubric):
        """Analiza el trabajo comparándolo con la rúbrica activa."""
        work_lower = work_text.lower()
        details = []
        total_points = 0
        
        for criterion in rubric['criteria']:
            # Lógica de coincidencia semántica simple para la simulación
            match_score = 0
            keywords = criterion.lower().split()
            found = [w for w in keywords if w in work_lower and len(w) > 3]
            
            if len(found) > 0:
                match_score = min(10, 5 + len(found))
                evidence = f"Se detectó concordancia con términos: {', '.join(found[:2])}..."
                feedback = "Buen alineamiento con los requisitos del criterio."
            else:
                match_score = 4
                evidence = "No se encontraron referencias explícitas a este criterio."
                feedback = "Es necesario profundizar en este aspecto específico."
            
            details.append({
                "criterio": criterion,
                "puntos": match_score,
                "evidencia": evidence,
                "feedback": feedback
            })
            total_points += match_score

        return {
            "nota": round((total_points / (len(rubric['criteria']) * 10)) * 10, 1),
            "detalles": details,
            "mensaje": "Evaluación finalizada comparando el trabajo con los criterios definidos en la rúbrica activa."
        }

    def _display_detailed_report(self, results, source_name, rubric_name):
        console.print(f"\n[bold white]Trabajo:[/bold white] [yellow]{source_name}[/yellow] | [bold white]Rúbrica:[/bold white] [cyan]{rubric_name}[/cyan]")
        
        table = Table(show_header=True, header_style="bold magenta", box=None)
        table.add_column("Criterio de la Rúbrica", style="cyan")
        table.add_column("Pts", justify="center", style="bold green")
        table.add_column("Evidencia de Cumplimiento", style="dim italic")
        
        for d in results['detalles']:
            table.add_row(d['criterio'], str(d['puntos']), d['evidencia'])
        
        console.print(table)
        
        nota = results['nota']
        color = "green" if nota >= 7 else "yellow" if nota >= 5 else "red"
        console.print(f"\n[bold white]Calificación Justificada:[/bold white] [bold {color}]{nota}/10.0[/bold {color}]")
        
        # Feedback Pedagógico consolidado
        feedback_text = "\n".join([f"• {d['criterio']}: {d['feedback']}" for d in results['detalles']])
        console.print(Panel(feedback_text, title="💬 RECOMENDACIONES DE MEJORA", border_style="yellow"))
        console.print("\n[dim center]SEA Engine v3.0 | Docensas 2026[/dim center]")

    def _evaluate_demo(self):
        console.print("\n[dim]Iniciando modo demostración... Arrastre un archivo real para un análisis completo.[/dim]")
        # (Aquí podría ir la lógica de demo anterior si se desea)

if __name__ == "__main__":
    try:
        sea = RubricAuditorSEA()
        path = sys.argv[1] if len(sys.argv) > 1 else None
        sea.process_input(path)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        console.print(f"[bold red]FATAL ERROR:[/bold red] {str(e)}")
    finally:
        console.print("\n[bold cyan]Proceso finalizado. Presione Enter para salir...[/bold cyan]")
        input()
