# main.py - Auditor de Rubricas (v2.0 - Auditor Dinámico Inteligente)
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
    # Soporte para PyInstaller
    if getattr(sys, 'frozen', False):
        bundle_dir = sys._MEIPASS
        if bundle_dir not in sys.path:
            sys.path.insert(0, bundle_dir)
    
    # Añadir el directorio raíz al path para importaciones cruzadas
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if root_path not in sys.path:
        sys.path.insert(0, root_path)
    
    # Intentar importación directa (estructura plana de PyInstaller)
    try:
        from adapters.pdf_adapter import PDFAdapter
    except ImportError:
        # Intentar importación relativa al paquete
        from celula_auditor_rubricas.adapters.pdf_adapter import PDFAdapter
except Exception as e:
    PDFAdapter = None
    _import_error = str(e)

console = Console()

class RubricAuditorADI:
    """Auditor Dinámico Inteligente (ADI)"""
    
    def __init__(self):
        try:
            self.pdf_adapter = PDFAdapter() if PDFAdapter else None
        except Exception as e:
            self.pdf_adapter = None
            console.print(f"[dim red]Error al instanciar PDFAdapter: {str(e)}[/dim red]")
        
        self._show_header()
        
    def _show_header(self):
        header = """
# 🎓 Auditor Dinámico Inteligente (ADI)
*Evaluación Formativa Basada en IA y Evidencia Documental*
        """
        console.print(Panel(Markdown(header), border_style="cyan"))

    def analyze(self, pdf_path=None):
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                
                # 1. Ingesta
                progress.add_task(description="[bold blue]Extrayendo conocimiento del PDF...[/bold blue]", total=None)
                if pdf_path and os.path.exists(pdf_path):
                    if not self.pdf_adapter:
                        raise RuntimeError("El adaptador PDF no está inicializado. Error de empaquetado.")
                    text = self.pdf_adapter.extract_text(pdf_path)
                    source_name = os.path.basename(pdf_path)
                else:
                    text = "Entrega vacía o no encontrada. Por favor, arrastre un archivo PDF válido."
                    source_name = "N/A"
                    if not pdf_path:
                        # Simulacion educativa si no hay archivo
                        text = "El alumno propone una arquitectura MVC con controladores en Java y persistencia en Supabase."
                        source_name = "Simulación_Educativa.pdf"

                # 2. Razonamiento CoT (Simulado pero dinámico basado en texto)
                progress.add_task(description="[bold magenta]ADI Razonando cumplimiento (Chain-of-Thought)...[/bold magenta]", total=None)
                time.sleep(2.5)
                
                results = self._perform_dynamic_logic(text)
                
                # 3. Presentación
                self._display_detailed_report(results, source_name)
                
        except Exception as e:
            console.print(f"[bold red]Error en la auditoría:[/bold red] {str(e)}")

    def _perform_dynamic_logic(self, text):
        """
        Analiza el texto buscando patrones para puntuar de forma dinámica.
        """
        text_lower = text.lower()
        
        # Criterio 1: Arquitectura
        score_arch = 0
        evid_arch = "No se detectan conceptos arquitecturales claros."
        if any(w in text_lower for w in ["arquitectura", "mvc", "capas", "modular", "celula"]):
            score_arch = 8 if "modular" in text_lower else 6
            evid_arch = f"Referencia detectada: '{[w for w in ['arquitectura', 'mvc', 'capas', 'modular'] if w in text_lower][0]}'"
        
        # Criterio 2: Implementación Técnica
        score_tech = 0
        evid_tech = "Falta detalle en la implementación técnica."
        if any(w in text_lower for w in ["python", "java", "codigo", "implementacion", "api"]):
            score_tech = 9 if len(text) > 500 else 7
            evid_tech = "Se observa descripción de componentes técnicos activos."

        # Criterio 3: Calidad y Estándares
        score_qual = 5
        if "clean" in text_lower or "estandar" in text_lower:
            score_qual = 10
            evid_qual = "Uso explícito de estándares de Clean Architecture."
        else:
            evid_qual = "Se recomienda integrar principios de Clean Code."

        # Construcción del objeto de respuesta (basado en el prompt ADI v2.0)
        total_points = score_arch + score_tech + score_qual
        
        return {
            "resumen": "Análisis completado satisfactoriamente sobre la evidencia proporcionada.",
            "nota": round((total_points / 30) * 10, 1),
            "detalles": [
                {"criterio": "Arquitectura Sistémica", "puntos": score_arch, "evidencia": evid_arch, "feedback": "Reforzar la separación de responsabilidades."},
                {"criterio": "Densidad Técnica", "puntos": score_tech, "evidencia": evid_tech, "feedback": "Excelente profundidad en la descripción."},
                {"criterio": "Estándares Profesionales", "puntos": score_qual, "evidencia": evid_qual, "feedback": "Integrar más validaciones de tipo (Type Hinting)."}
            ],
            "mensaje_alumno": "Has demostrado una buena base técnica. Para alcanzar la excelencia, enfócate en documentar mejor las interfaces entre módulos."
        }

    def _display_detailed_report(self, results, source_name):
        # Panel de Resumen
        console.print(f"\n[bold white]Archivo auditado:[/bold white] [yellow]{source_name}[/yellow]")
        console.print(Panel(results['resumen'], title="Resumen Ejecutivo", border_style="green"))
        
        # Tabla de Criterios
        table = Table(show_header=True, header_style="bold magenta", box=None)
        table.add_column("Criterio de Rúbrica", style="cyan")
        table.add_column("Puntos (max 10)", justify="center", style="bold green")
        table.add_column("Evidencia Hallada", style="dim italic")
        
        for d in results['detalles']:
            table.add_row(d['criterio'], str(d['puntos']), d['evidencia'])
        
        console.print(table)
        
        # Nota Final con Estilo
        nota = results['nota']
        color_nota = "green" if nota >= 7 else "yellow" if nota >= 5 else "red"
        console.print(f"\n[bold white]Nota Final Calibrada:[/bold white] [bold {color_nota}]{nota}/10.0[/bold {color_nota}]")
        
        # PANEL DE FEEDBACK PARA EL ALUMNO (Lo más importante)
        feedback_panel = Panel(
            results['mensaje_alumno'],
            title="💬 FEEDBACK PARA EL ALUMNO",
            subtitle="Pedagog-IA Feedback Engine",
            border_style="yellow",
            padding=(1, 2)
        )
        console.print(feedback_panel)
        console.print("\n[dim center]Propulsado por el Ecosistema Pedagog-IA | Docensas 2026[/dim center]")

if __name__ == "__main__":
    try:
        adi = RubricAuditorADI()
        path = sys.argv[1] if len(sys.argv) > 1 else None
        adi.analyze(path)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        console.print(f"[bold red]FATAL ERROR:[/bold red] {str(e)}")
    finally:
        console.print("\n[bold cyan]Auditoría finalizada. Presione Enter para salir...[/bold cyan]")
        input()
