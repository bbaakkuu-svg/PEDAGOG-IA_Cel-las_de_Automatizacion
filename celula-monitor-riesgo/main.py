# main.py - Monitor de Alumnos en Riesgo (EWS)
# -------------------------------------------------------------------------
from core.analyzer import RiskAnalyzer
import rich
from rich.console import Console
from rich.table import Table
import os

console = Console()

def run_monitor():
    data_file = os.path.join("data", "logs_ejemplo.csv")
    
    console.print("[bold yellow]🚀 Iniciando Monitor de Alumnos en Riesgo (EWS)...[/bold yellow]")
    
    try:
        analyzer = RiskAnalyzer(data_file)
        results = analyzer.calculate_risk()
        
        # Crear tabla visual
        table = Table(title="Reporte de Riesgo de Abandono")
        table.add_column("Estudiante ID", style="cyan")
        table.add_column("Score", justify="right", style="magenta")
        table.add_column("Nivel", style="bold")
        table.add_column("Intervencion", justify="center")

        for _, row in results.iterrows():
            color = "red" if row['risk_level'] == "CRITICO" else "yellow" if row['risk_level'] == "MEDIO" else "green"
            table.add_row(
                row['student_id'],
                str(row['risk_score']),
                f"[{color}]{row['risk_level']}[/{color}]",
                "⚠️ SI" if row['action_needed'] else "✅ NO"
            )

        console.print(table)
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")

if __name__ == "__main__":
    run_monitor()
