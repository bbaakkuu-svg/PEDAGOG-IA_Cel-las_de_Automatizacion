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
root_path = Path(__file__).parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

# Integración de IA-Ops Observability (Independiente)
try:
    from infra.observability import default_logger, InteractionStatus
except ImportError:
    default_logger = None
    InteractionStatus = None

# Núcleo del Ecosistema
try:
    from core.config import Config
    from core.adapters.pdf_adapter import PDFAdapter
    from core.adapters.excel_adapter import ExcelExporter
    from core.cache import FileCache
except ImportError:
    Config = None
    PDFAdapter = None
    ExcelExporter = None
    FileCache = None

# Manejo de dependencias (se mantiene para compatibilidad con librerías externas)
PDF_SUPPORT = True if PDFAdapter else False
EXCEL_SUPPORT = True if ExcelExporter else False

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
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
            self.cache = FileCache("auditor") if FileCache else None
        except NameError:
            self.exporter = None
            self.cache = None
            
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
        """Procesa masivamente todos los archivos válidos en un directorio usando concurrencia."""
        import concurrent.futures
        
        valid_extensions = (".pdf", ".txt", ".json")
        files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.lower().endswith(valid_extensions)]
        
        if not files:
            console.print("[bold yellow]⚠️ No se encontraron archivos evaluables en el directorio.[/bold yellow]")
            return

        if not os.path.exists(self.config_path):
            console.print("[bold red]✘ Error: Configure una rúbrica antes de iniciar el procesamiento por lotes.[/bold red]")
            return

        console.print(Panel(f"[bold cyan]🚀 Iniciando Modo Batch Pro (Concurrente):[/bold cyan] {len(files)} archivos.", border_style="blue"))
        
        success_count = 0
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            transient=False
        ) as progress:
            batch_task = progress.add_task(f"[bold cyan]Evaluando lote...", total=len(files))
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                # Mapear archivos a futuros
                future_to_file = {executor.submit(self._evaluate_work, f, quiet=True): f for f in files}
                
                for future in concurrent.futures.as_completed(future_to_file):
                    file_path = future_to_file[future]
                    try:
                        success = future.result()
                        if success:
                            success_count += 1
                        progress.update(batch_task, advance=1, description=f"[blue]Completado: {os.path.basename(file_path)}[/blue]")
                    except Exception as e:
                        console.print(f"[red]✘ Error crítico en {os.path.basename(file_path)}: {e}[/red]")
                        progress.update(batch_task, advance=1)
        
        console.print(f"\n[bold green]✅ Proceso masivo finalizado.[/bold green] ({success_count}/{len(files)} exitosos)")
        console.print(f"[dim]Resultados consolidados en: {self.excel_path}[/dim]\n")

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
                
                # Clave de caché: contenido del trabajo + criterios de la rúbrica
                cache_key = work_text + json.dumps(rubric['criteria'])
                cached_results = self.cache.get(cache_key) if self.cache else None
                
                if cached_results:
                    if not quiet:
                        console.print("[dim]⚡ Resultado recuperado de caché (acelerado).[/dim]")
                    results = cached_results
                else:
                    start_time = time.time()
                    try:
                        results = self._perform_comparative_analysis(work_text, rubric)
                        latency_ms = (time.time() - start_time) * 1000
                        
                        # Registro de telemetría (Éxito)
                        if default_logger:
                            default_logger.log_interaction(
                                cell_id="auditor",
                                model_id="local-sea-v4", # En este caso es el engine local
                                latency_ms=latency_ms,
                                prompt_tokens=len(work_text.split()), # Estimación simple
                                completion_tokens=len(json.dumps(results).split()),
                                status=InteractionStatus.SUCCESS,
                                metadata={"file": os.path.basename(path)}
                            )
                    except Exception as e:
                        latency_ms = (time.time() - start_time) * 1000
                        if default_logger:
                            default_logger.log_interaction(
                                cell_id="auditor",
                                model_id="local-sea-v4",
                                latency_ms=latency_ms,
                                status=InteractionStatus.FAILURE,
                                error_message=str(e)
                            )
                        raise e
                    
                    if self.cache:
                        self.cache.set(cache_key, results)
                
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
                
                # Exportar a JSON para el Cerebro Central
                output_dir = os.path.join(root_path, "output", "evaluations")
                os.makedirs(output_dir, exist_ok=True)
                json_output_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(path))[0]}.json")
                
                eval_for_brain = {
                    "student_id": os.path.splitext(os.path.basename(path))[0],
                    "source_file": os.path.basename(path),
                    "nota": results['nota'],
                    "detalles": results['detalles'],
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                
                with open(json_output_path, "w", encoding="utf-8") as f:
                    json.dump(eval_for_brain, f, indent=4, ensure_ascii=False)

                # Reporte en consola si no es modo batch (quiet)
                if not quiet:
                    self._display_detailed_report(results, os.path.basename(path), rubric['source'])
                    console.print(f"[dim]Data persistida para el Cerebro Central en: {os.path.basename(json_output_path)}[/dim]")
                
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
