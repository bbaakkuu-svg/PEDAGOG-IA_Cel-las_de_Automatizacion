import sys
import os
import time
from datetime import datetime

# Añadir el path del proyecto para importar infra
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from infra.observability import default_logger, CostCalculator, InteractionStatus

def test_observability():
    print("--- TEST DE OBSERVABILIDAD IA-OPS ---")
    
    # 1. Simular interacciones
    print("Simulando interacciones...")
    
    # Interaccion 1: Auditoria Exitosa
    default_logger.log_interaction(
        cell_id="auditor",
        model_id="gemini-1.5-pro",
        latency_ms=1250.5,
        prompt_tokens=1500,
        completion_tokens=500,
        status=InteractionStatus.SUCCESS,
        metadata={"rubric_id": "math_v1"}
    )
    
    # Interaccion 2: Generacion Rapida
    default_logger.log_interaction(
        cell_id="generator",
        model_id="gemini-1.5-flash",
        latency_ms=450.2,
        prompt_tokens=800,
        completion_tokens=1200,
        status=InteractionStatus.SUCCESS
    )
    
    # Interaccion 3: Error de Red
    default_logger.log_interaction(
        cell_id="monitor",
        model_id="gpt-4o",
        latency_ms=2000.0,
        status=InteractionStatus.FAILURE,
        error_message="API connection timeout"
    )
    
    print("Interacciones registradas.")
    
    # 2. Analizar logs
    date_str = datetime.now().strftime("%Y-%m-%d")
    log_file = f"data/logs/observability/ia_ops_{date_str}.jsonl"
    
    print(f"\nAnalizando logs en: {log_file}")
    report = CostCalculator.analyze_logs(log_file)
    
    print("\n--- REPORTE DE IA-OPS ---")
    print(f"Costo Total Estimado: ${report['total_estimated_cost']}")
    print(f"Total Tokens: {report['total_tokens']}")
    print(f"Tasa de Exito: {report['success_rate']*100}%")
    print(f"Latencia Media: {report['avg_latency_ms']} ms")

if __name__ == "__main__":
    test_observability()
