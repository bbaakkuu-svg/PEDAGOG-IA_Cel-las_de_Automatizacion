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
        Calcula el nivel de riesgo con resiliencia (Graceful Degradation).
        Soporta tanto datasets completos de logs como reportes parciales del Auditor.
        """
        final_results = []
        for row in self.data:
            score = 0
            
            # Helper para convertir a float/int seguro
            def safe_val(key, default=None):
                val = row.get(key)
                if val is None or str(val).strip() == '':
                    return default
                try:
                    return float(val)
                except:
                    return default

            # Extracción flexible de variables (Data Contract)
            student_id = row.get('student_id', row.get('id', 'N/A'))
            grade = safe_val('nota_media', safe_val('avg_grade'))
            
            # Variables de log de plataforma (pueden no existir si viene del Auditor)
            last_login = safe_val('last_login_days', safe_val('login_days'))
            sub_rate = safe_val('submission_rate', safe_val('tasa_entrega'))
            posts = safe_val('forum_posts', safe_val('posts_foro'))

            # Lógica de Pesos Dinámicos
            if last_login is None and sub_rate is None and posts is None:
                # MODO AUDITOR: Solo tenemos la nota media. El peso recae 100% en el rendimiento.
                if grade is not None:
                    if grade < 5: score += 70  # Suspenso directo -> Riesgo Crítico
                    elif grade < 7: score += 40 # Aprobado justo -> Riesgo Medio
            else:
                # MODO COMPLETO: Datos de plataforma + Notas
                if last_login is not None and last_login > 7: score += 40
                if sub_rate is not None and sub_rate < 0.5: score += 30
                if grade is not None and grade < 5: score += 20
                if posts is not None and posts < 2: score += 10

            # Determinación del nivel
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
