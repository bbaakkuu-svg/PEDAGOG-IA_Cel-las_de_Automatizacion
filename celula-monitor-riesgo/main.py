# main.py - Monitor de Alumnos en Riesgo (EWS) - SLIM VERSION
# -------------------------------------------------------------------------
import os
import sys
import time

# Manejo de dependencias con reporte amigable
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt
    from rich.live import Live
    from rich.spinner import Spinner
except ImportError:
    print("Error: Soporte para 'rich' no disponible. Instale 'rich'.")
    sys.exit(1)

try:
    from core.analyzer import RiskAnalyzer
except ImportError as e:
    # Resolución de ruta para empaquetado
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    try:
        from core.analyzer import RiskAnalyzer
    except ImportError:
        print(f"Error crítico: Módulos del núcleo no encontrados. ({e})")
        sys.exit(1)

console = Console()

class RiskMonitorSEA:
    def __init__(self):
        self.default_data = os.path.join("data", "logs_ejemplo.csv")
        self._ensure_data_exists()

    def _ensure_data_exists(self):
        """Crea un archivo de ejemplo si no existe usando csv nativo."""
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(self.default_data):
            import csv
            data = [
                ["student_id", "last_login_days", "submission_rate", "avg_grade", "forum_posts"],
                ["ALUM001", 10, 0.4, 4.5, 1],
                ["ALUM002", 2, 0.9, 8.5, 5],
                ["ALUM003", 8, 0.6, 5.5, 0]
            ]
            with open(self.default_data, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(data)

    def process_data(self, path: str):
        with Live(Spinner("bouncingBar", text="Analizando patrones de riesgo..."), refresh_per_second=10) as live:
            try:
                analyzer = RiskAnalyzer(path)
                results = analyzer.calculate_risk() # Lista de dicts
                
                time.sleep(1.2) # Efecto visual de análisis profundo

                # Crear tabla visual
                table = Table(title=f"📊 Reporte de Riesgo: {os.path.basename(path)}", border_style="yellow")
                table.add_column("Estudiante ID", style="cyan")
                table.add_column("Score", justify="right", style="magenta")
                table.add_column("Nivel de Riesgo", style="bold")
                table.add_column("Intervención", justify="center")

                for row in results:
                    level = row['risk_level']
                    color = "red" if level == "CRITICO" else "yellow" if level == "MEDIO" else "green"
                    
                    table.add_row(
                        str(row['student_id']),
                        str(row['risk_score']),
                        f"[{color}]{level}[/{color}]",
                        "🚨 URGENTE" if level == "CRITICO" else "⚠️ RECOMENDADA" if level == "MEDIO" else "✅ ESTABLE"
                    )

                live.update(table)
                
            except Exception as e:
                live.update(Panel(f"[bold red]✘ Error en el análisis:[/bold red]\n{e}", border_style="red"))

    def run_interactive(self):
        console.print(Panel.fit(
            "[bold yellow]PEDAGOG-IA: Monitor de Alumnos en Riesgo (EWS) [SLIM][/bold yellow]\n"
            "[dim]Early Warning System v1.1 | Antigravity 2026[/dim]",
            border_style="yellow"
        ))

        while True:
            console.print("\n[bold white]Opciones:[/bold white]")
            console.print(" 1. Arrastrar archivo de datos (.csv, .xlsx)")
            console.print(" 2. Ejecutar análisis con datos de ejemplo")
            console.print(" 3. Salir")
            
            choice = Prompt.ask("\nSeleccione una opción", choices=["1", "2", "3"], default="2")
            
            if choice == "1":
                path = Prompt.ask("Arrastre el archivo (CSV/Excel) aquí y presione Enter").strip('"').strip("'")
                if os.path.exists(path):
                    self.process_data(path)
                else:
                    console.print("[bold red]Archivo no encontrado.[/bold red]")
            
            elif choice == "2":
                self.process_data(self.default_data)
            
            elif choice == "3":
                console.print("[yellow]Saliendo...[/yellow]")
                break

if __name__ == "__main__":
    app = RiskMonitorSEA()
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if os.path.exists(path):
            app.process_data(path)
            input("\nPresione Enter para salir...")
    else:
        app.run_interactive()
