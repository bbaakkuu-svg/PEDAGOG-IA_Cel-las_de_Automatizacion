# analyzer.py - Logica de deteccion de riesgo de abandono (SLIM VERSION - NO PANDAS)
# -------------------------------------------------------------------------
import os
import csv

try:
    from openpyxl import load_workbook
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False

class RiskAnalyzer:
    def __init__(self, data_path: str):
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"No se encuentra el archivo de datos: {data_path}")
        
        self.data_path = data_path
        self.data = self._load_data() # Lista de dicts

    def _load_data(self):
        """Carga datos desde CSV o Excel sin usar pandas."""
        ext = os.path.splitext(self.data_path)[1].lower()
        results = []
        
        try:
            if ext == '.csv':
                with open(self.data_path, mode='r', encoding='utf-8-sig') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        results.append({k.strip().lower(): v for k, v in row.items()})
            
            elif ext in ['.xlsx', '.xls']:
                if not HAS_OPENPYXL:
                    raise ImportError("Soporte para Excel no instalado (openpyxl).")
                
                wb = load_workbook(self.data_path, data_only=True)
                ws = wb.active # Toma la hoja activa
                headers = [str(cell.value).strip().lower() for cell in ws[1]]
                
                for row in ws.iter_rows(min_row=2, values_only=True):
                    if not any(row): continue
                    results.append(dict(zip(headers, row)))
            else:
                raise ValueError(f"Formato no soportado: {ext}")
            
            return results
        except Exception as e:
            raise RuntimeError(f"Error al leer {ext}: {e}")

    def calculate_risk(self):
        """
        Calcula el nivel de riesgo (vía diccionarios).
        """
        final_results = []
        for row in self.data:
            score = 0
            
            # Helper para convertir a float/int seguro
            def safe_val(key, default=0):
                val = row.get(key, default)
                try:
                    return float(val) if val is not None else default
                except:
                    return default

            last_login = safe_val('last_login_days', safe_val('login_days', 0))
            sub_rate = safe_val('submission_rate', safe_val('tasa_entrega', 1.0))
            grade = safe_val('avg_grade', safe_val('nota_media', 10.0))
            posts = safe_val('forum_posts', safe_val('posts_foro', 5))
            student_id = row.get('student_id', row.get('id', 'N/A'))

            if last_login > 7: score += 40
            if sub_rate < 0.5: score += 30
            if grade < 5: score += 20
            if posts < 2: score += 10

            level = "BAJO"
            if score >= 70: level = "CRITICO"
            elif score >= 40: level = "MEDIO"

            final_results.append({
                "student_id": student_id,
                "risk_score": score,
                "risk_level": level,
                "action_needed": level != "BAJO"
            })
        
        return final_results
