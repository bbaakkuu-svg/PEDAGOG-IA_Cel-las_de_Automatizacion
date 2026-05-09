import pandas as pd
import os
import json
import glob
from pathlib import Path
from datetime import datetime

# Importación defensiva del logger
try:
    from core.logger import setup_logger
    logger = setup_logger("DataEngine")
except ImportError:
    import logging
    logger = logging.getLogger("DataEngine")

class DataEngine:
    def __init__(self, root_path):
        self.root_path = Path(root_path)
        self.excel_path = self.root_path / "cells/auditor/Registro_Evaluaciones_PedagogIA.xlsx"
        self.logs_dir = self.root_path / "data/logs/observability"
        self.evals_dir = self.root_path / "output/evaluations"
        self.reinf_dir = self.root_path / "output/reinforcement"

    def get_dashboard_data(self):
        data = {
            "stats": {
                "total_evaluaciones": 0,
                "total_reforzamientos": 0,
                "costo_total_usd": 0.0,
                "latencia_media_ms": 0.0
            },
            "ia_ops": [],
            "recent_cycles": [],
            "last_update": datetime.now().strftime("%H:%M:%S")
        }

        # 1. Cargar Estadísticas IA-Ops
        self._load_ia_ops(data)

        # 2. Cargar Ciclos Pedagógicos
        self._load_pedagogical_cycles(data)

        # 3. Cargar datos del Auditor (Excel) - Opcional para este dashboard pro
        self._load_excel_stats(data)

        return data

    def _load_ia_ops(self, data):
        """Lee los logs de observability para calcular costos y rendimiento."""
        log_files = glob.glob(str(self.logs_dir / "*.jsonl"))
        all_interactions = []
        
        total_latency = 0
        count = 0
        total_cost = 0.0

        # Precios (Simulados de CostCalculator)
        PRICES = {"gemini-1.5-pro": 0.0035, "gemini-1.5-flash": 0.00035, "gpt-4o": 0.005}

        for log_file in log_files:
            try:
                with open(log_file, "r", encoding="utf-8") as f:
                    for line in f:
                        item = json.loads(line)
                        all_interactions.append(item)
                        
                        # Cálculos
                        total_latency += item.get("latency_ms", 0)
                        count += 1
                        
                        model = item.get("model_id", "unknown")
                        tokens = item.get("total_tokens", 0)
                        price_per_1k = PRICES.get(model, 0.001)
                        total_cost += (tokens / 1000) * price_per_1k
            except Exception as e:
                logger.error(f"Error procesando log {log_file}: {e}")

        data["stats"]["costo_total_usd"] = round(total_cost, 4)
        data["stats"]["latencia_media_ms"] = round(total_latency / count, 2) if count > 0 else 0
        data["ia_ops"] = all_interactions[-10:] # Últimos 10 eventos

    def _load_pedagogical_cycles(self, data):
        """Mapea las evaluaciones con sus respectivos refuerzos."""
        if not self.evals_dir.exists():
            return

        eval_files = glob.glob(str(self.evals_dir / "*.json"))
        data["stats"]["total_evaluaciones"] = len(eval_files)

        for eval_file in eval_files:
            try:
                with open(eval_file, "r", encoding="utf-8") as f:
                    eval_data = json.load(f)
                
                student_id = eval_data.get("student_id")
                # Verificar si tiene refuerzo
                reinf_plan = self.reinf_dir / f"plan_{student_id}.json"
                has_reinforcement = reinf_plan.exists()
                
                if has_reinforcement:
                    data["stats"]["total_reforzamientos"] += 1
                
                data["recent_cycles"].append({
                    "student": student_id,
                    "grade": eval_data.get("nota"),
                    "status": "Reforzado" if has_reinforcement else "Pendiente",
                    "timestamp": eval_data.get("timestamp")
                })
            except Exception as e:
                logger.error(f"Error cargando ciclo: {e}")

        # Ordenar por fecha
        data["recent_cycles"].sort(key=lambda x: x['timestamp'], reverse=True)

    def _load_excel_stats(self, data):
        # Mantenemos compatibilidad con el Excel si existe
        if os.path.exists(self.excel_path):
            try:
                df = pd.read_excel(self.excel_path)
                data["stats"]["total_historico"] = len(df)
            except:
                pass
