# main.py - Sistema de Evaluación Adaptativo (SEA) v4.0 - Data-Driven Insight
# -------------------------------------------------------------------------
import sys
import os
import time
import json

# Forzar codificación UTF-8 en Windows para evitar errores con emojis y caracteres especiales
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Resolución de rutas para acceder al núcleo compartido
from pathlib import Path
root_path = Path(__file__).parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

try:
    from pedagogia_shared import Config
    from pedagogia_shared.adapters.pdf_adapter import PDFAdapter
    from pedagogia_shared.adapters.excel_adapter import ExcelExporter
except ImportError:
    Config = None
    PDFAdapter = None
    ExcelExporter = None

# Manejo de dependencias (se mantiene para compatibilidad con librerías externas)
PDF_SUPPORT = True if PDFAdapter else False
EXCEL_SUPPORT = True if ExcelExporter else False

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown

console = Console()

class RubricAuditorSEA:
    """Sistema de Evaluación Adaptativo (SEA) v4.0"""
    
    def __init__(self):
        # Inicialización defensiva
        try:
            self.pdf_adapter = PDFAdapter() if PDF_SUPPORT else None
        except NameError:
            self.pdf_adapter = None
            
        # Directorio base para archivos persistentes
        base_dir = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
        self.config_path = os.path.join(base_dir, "active_rubric.json")
        self.excel_path = os.path.join(base_dir, "Registro_Evaluaciones_PedagogIA.xlsx")
        
        try:
            self.exporter = ExcelExporter(self.excel_path) if EXCEL_SUPPORT else None
        except NameError:
            self.exporter = None
            
        self._show_header()
        
    def _show_header(self):
        rubric_status = "[bold green]Cargada[/bold green]" if os.path.exists(self.config_path) else "[bold red]No definida[/bold red]"
        header = f"""
# 🎓 SEA v4.0: Data-Driven Insight
*Estado de la Rúbrica:* {rubric_status} | *Registro Excel:* [dim]{os.path.basename(self.excel_path)}[/dim]

**Instrucciones:**
1. Arrastra una **rúbrica** para configurar criterios.
2. Arrastra **trabajos** para evaluarlos.
3. Los resultados se guardan automáticamente en Excel.
        """
        console.print(Panel(Markdown(header), border_style="cyan"))
        
        if Config and Config.DEBUG:
            console.print(f"[dim]Configuración activa desde .env (Raíz: {Config.PROJECT_ROOT})[/dim]")

    def process_input(self, path):
        if not path or not os.path.exists(path):
            self._evaluate_demo()
            return

        if os.path.isdir(path):
            self._evaluate_batch(path)
        elif path.lower().endswith((".txt", ".json", ".pdf")):
            filename = os.path.basename(path).lower()
            if "rubrica" in filename or "criterios" in filename:
                self._ingest_rubric(path)
            else:
                self._evaluate_work(path)
        else:
            console.print("[bold yellow]⚠️ Formato no soportado (use .pdf, .txt o .json).[/bold yellow]")

    def _evaluate_batch(self, directory_path):
        """Procesa masivamente todos los archivos válidos en un directorio."""
        valid_extensions = (".pdf", ".txt", ".json")
        files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.lower().endswith(valid_extensions)]
        
        if not files:
            console.print("[bold yellow]⚠️ No se encontraron archivos evaluables en el directorio.[/bold yellow]")
            return

        if not os.path.exists(self.config_path):
            console.print("[bold red]✘ Error: Configure una rúbrica antes de iniciar el procesamiento por lotes.[/bold red]")
            return

        console.print(Panel(f"[bold cyan]🚀 Iniciando Modo Batch:[/bold cyan] {len(files)} archivos encontrados.", border_style="blue"))
        
        success_count = 0
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=False
        ) as progress:
            batch_task = progress.add_task(f"[bold cyan]Procesando lote...", total=len(files))
            
            for file_path in files:
                progress.update(batch_task, description=f"[blue]Evaluando: {os.path.basename(file_path)}[/blue]")
                try:
                    success = self._evaluate_work(file_path, quiet=True)
                    if success:
                        success_count += 1
                except Exception as e:
                    console.print(f"[red]✘ Error procesando {os.path.basename(file_path)}: {e}[/red]")
                
                progress.advance(batch_task)
        
        console.print(f"\n[bold green]✅ Proceso por lotes finalizado.[/bold green] ({success_count}/{len(files)} exitosos)")
        console.print(f"[dim]Los resultados se han consolidado en: {self.excel_path}[/dim]\n")

    def _ingest_rubric(self, path):
        try:
            console.print(f"\n[bold blue]⚙️ Configurando nueva rúbrica desde:[/bold blue] {os.path.basename(path)}")
            
            # Validación preventiva para PDF
            if path.lower().endswith(".pdf"):
                if not self.pdf_adapter:
                    raise RuntimeError("Soporte para PDF no disponible. Instale 'pymupdf'.")
                text = self.pdf_adapter.extract_text(path)
            try:
                text = open(path, 'r', encoding='utf-8').read()
            except UnicodeDecodeError:
                text = open(path, 'r', encoding='latin-1').read()
            
            rubric_data = {
                "source": os.path.basename(path),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "criteria": self._extract_criteria_from_text(text)
            }
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(rubric_data, f, indent=4)
            
            console.print("[bold green]✅ Rúbrica configurada. SEA v4.0 listo para evaluar y registrar datos.[/bold green]")
        except Exception as e:
            console.print(f"[bold red]Error al cargar la rúbrica:[/bold red] {str(e)}")

    def _extract_criteria_from_text(self, text):
        lines = [line.strip() for line in text.split('\n') if len(line.strip()) > 10]
        if len(lines) > 3:
            return [lines[i][:50] for i in range(min(5, len(lines)))]
        return ["Calidad Técnica", "Documentación", "Arquitectura", "Innovación"]

    def _evaluate_work(self, path, quiet=False):
        if not os.path.exists(self.config_path):
            console.print("[bold yellow]⚠️ No hay una rúbrica activa.[/bold yellow]")
            return

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                rubric = json.load(f)

            with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
                progress.add_task(description=f"[bold blue]Evaluando: {os.path.basename(path)}...[/bold blue]", total=None)
                
                # Validación preventiva para PDF
                if path.lower().endswith(".pdf"):
                    if not self.pdf_adapter:
                        raise RuntimeError("Soporte para PDF no disponible. Instale 'pymupdf'.")
                    work_text = self.pdf_adapter.extract_text(path)
                else:
                    try:
                        work_text = open(path, 'r', encoding='utf-8').read()
                    except UnicodeDecodeError:
                        work_text = open(path, 'r', encoding='latin-1').read()
                
                time.sleep(2)
                
                results = self._perform_comparative_analysis(work_text, rubric)
                
                # Exportar a Excel automáticamente
                if self.exporter:
                    summary = ", ".join([f"{d['criterio']} ({d['puntos']})" for d in results['detalles']])
                    estado = "Sobresaliente" if results['nota'] >= 9 else "Notable" if results['nota'] >= 7 else "Aprobado" if results['nota'] >= 5 else "Insuficiente"
                    self.exporter.add_row(
                        entity_id=os.path.splitext(os.path.basename(path))[0],
                        source_file=os.path.basename(path),
                        process_type=f"Auditoria ({rubric['source']})",
                        value=results['nota'],
                        status_level=estado,
                        details=summary
                    )
                
                # Reporte en consola si no es modo batch (quiet)
                if not quiet:
                    self._display_detailed_report(results, os.path.basename(path), rubric['source'])
                
                return True
        except Exception as e:
            if not quiet:
                console.print(f"[bold red]Error en la evaluación:[/bold red] {str(e)}")
            return False

    def _perform_comparative_analysis(self, work_text, rubric):
        work_lower = work_text.lower()
        details = []
        total_points = 0
        
        for criterion in rubric['criteria']:
            match_score = 0
            keywords = criterion.lower().split()
            found = [w for w in keywords if w in work_lower and len(w) > 3]
            
            if len(found) > 0:
                match_score = min(10, 5 + len(found))
                evidence = f"Cumplimiento detectado ({', '.join(found[:1])})."
                feedback = "Nivel de cumplimiento satisfactorio."
            else:
                match_score = 4
                evidence = "No se hallaron evidencias específicas."
                feedback = "Se recomienda incluir más referencias técnicas."
            
            details.append({"criterio": criterion, "puntos": match_score, "evidencia": evidence, "feedback": feedback})
            total_points += match_score

        return {
            "nota": round((total_points / (len(rubric['criteria']) * 10)) * 10, 1),
            "detalles": details
        }

    def _display_detailed_report(self, results, source_name, rubric_name):
        console.print(f"\n[bold white]Alumno:[/bold white] [yellow]{source_name}[/yellow] | [bold white]Rúbrica:[/bold white] [cyan]{rubric_name}[/cyan]")
        
        table = Table(show_header=True, header_style="bold magenta", box=None)
        table.add_column("Criterio Evaluado", style="cyan")
        table.add_column("Pts", justify="center", style="bold green")
        table.add_column("Evidencia", style="dim italic")
        
        for d in results['detalles']:
            table.add_row(d['criterio'], str(d['puntos']), d['evidencia'])
        
        console.print(table)
        
        nota = results['nota']
        color = "green" if nota >= 7 else "yellow" if nota >= 5 else "red"
        console.print(f"\n[bold white]Nota Final:[/bold white] [bold {color}]{nota}/10.0[/bold {color}]")
        
        feedback_text = "\n".join([f"• {d['criterio']}: {d['feedback']}" for d in results['detalles']])
        console.print(Panel(feedback_text, title="💬 FEEDBACK PEDAGÓGICO", border_style="yellow"))
        
        if self.exporter:
            console.print(f"[bold green]📊 Registro exportado a Excel:[/bold green] [dim]{os.path.basename(self.excel_path)}[/dim]")
            try:
                os.startfile(self.excel_path) # Auto-abrir reporte
            except:
                pass
        else:
            console.print("[bold yellow]⚠️ Registro Excel omitido (soporte no disponible).[/bold yellow]")
            
        console.print("\n[dim center]SEA Engine v4.0 | Pedagog-ia 2026[/dim center]")

    def _evaluate_demo(self):
        console.print("\n[dim]Modo SEA v4.0 Activo. Arrastre archivos para iniciar el registro masivo.[/dim]")

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
