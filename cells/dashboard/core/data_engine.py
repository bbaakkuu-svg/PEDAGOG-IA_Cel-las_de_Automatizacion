import pandas as pd
import os
import json
from pathlib import Path

try:
    from core.logger import setup_logger
    logger = setup_logger("DataEngine")
except ImportError:
    import logging
    logger = logging.getLogger("DataEngine")

class DataEngine:
    def __init__(self, excel_path, risk_json_path=None):
        self.excel_path = excel_path
        self.risk_json_path = risk_json_path

    def get_dashboard_data(self):
        data = {
            "stats": {"total_evaluaciones": 0, "nota_promedio": 0, "tasa_aprobacion": 0, "alerta_riesgo": 0},
            "competencies": [],
            "at_risk": [],
            "last_update": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # 1. Cargar datos del Auditor (Excel)
        if os.path.exists(self.excel_path):
            try:
                df = pd.read_excel(self.excel_path)
                df.columns = [c.lower() for c in df.columns]
                
                if 'entidad_id' in df.columns and 'valor_resultado' in df.columns:
                    df = df.dropna(subset=['entidad_id', 'valor_resultado'])
                    
                    data["stats"]["total_evaluaciones"] = len(df)
                    if len(df) > 0:
                        data["stats"]["nota_promedio"] = round(df['valor_resultado'].mean(), 2)
                        data["stats"]["tasa_aprobacion"] = round((df['valor_resultado'] >= 5).mean() * 100, 2)
                    
                    if 'detalles_resumen' in df.columns:
                        data["competencies"] = self._extract_competencies(df)
                logger.info(f"Datos del Auditor cargados: {len(df)} registros.")
            except Exception as e:
                logger.error(f"Error cargando Auditor data: {e}")

        # 2. Cargar datos del Monitor (JSON)
        if self.risk_json_path and os.path.exists(self.risk_json_path):
            try:
                with open(self.risk_json_path, 'r', encoding='utf-8') as f:
                    risk_data = json.load(f)
                    data["at_risk"] = [r for r in risk_data if r['risk_level'] != "BAJO"]
                    data["stats"]["alerta_riesgo"] = len(data["at_risk"])
                logger.info(f"Datos de Riesgo cargados: {len(data['at_risk'])} alertas.")
            except Exception as e:
                logger.error(f"Error cargando Risk data: {e}")

        return data

    def _extract_competencies(self, df):
        results = {}
        if 'detalles_resumen' not in df.columns:
            return []
            
        for details in df['detalles_resumen'].dropna():
            parts = str(details).split(', ')
            for part in parts:
                try:
                    if ' (' in part:
                        name = part.split(' (')[0]
                        score = float(part.split('(')[1].replace(')', ''))
                        if name not in results:
                            results[name] = []
                        results[name].append(score)
                except:
                    continue
        
        return [
            {"name": k, "value": round(sum(v)/len(v)*10, 2), "count": len(v)} 
            for k, v in results.items()
        ]
