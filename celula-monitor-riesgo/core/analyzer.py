# analyzer.py - Logica de deteccion de riesgo de abandono
# -------------------------------------------------------------------------
import pandas as pd
import os

class RiskAnalyzer:
    def __init__(self, data_path: str):
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"No se encuentra el archivo de datos: {data_path}")
        
        self.data_path = data_path
        self.df = self._load_data()
        self._normalize_columns()

    def _load_data(self) -> pd.DataFrame:
        """Carga datos desde CSV o Excel."""
        ext = os.path.splitext(self.data_path)[1].lower()
        try:
            if ext == '.csv':
                return pd.read_csv(self.data_path)
            elif ext in ['.xlsx', '.xls']:
                # Intenta leer la primera hoja por defecto
                return pd.read_excel(self.data_path)
            else:
                raise ValueError(f"Formato de archivo no soportado: {ext}. Use .csv o .xlsx")
        except Exception as e:
            raise RuntimeError(f"Error al leer el archivo {ext}: {e}")

    def _normalize_columns(self):
        """Normaliza los nombres de las columnas para evitar errores de mayúsculas/minúsculas."""
        if not self.df.empty:
            self.df.columns = [str(c).strip().lower() for c in self.df.columns]

    def calculate_risk(self):
        """
        Calcula el nivel de riesgo basado en reglas heuristicas.
        """
        if self.df.empty:
            return pd.DataFrame()

        results = []
        for _, row in self.df.iterrows():
            score = 0
            
            # Mapeo de columnas con fallback
            last_login = row.get('last_login_days', row.get('login_days', 0))
            sub_rate = row.get('submission_rate', row.get('tasa_entrega', 1.0))
            grade = row.get('avg_grade', row.get('nota_media', 10.0))
            posts = row.get('forum_posts', row.get('posts_foro', 5))
            student_id = row.get('student_id', row.get('id', 'N/A'))

            # Regla 1: Inactividad
            if last_login > 7: score += 40
            # Regla 2: Baja tasa de entrega
            if sub_rate < 0.5: score += 30
            # Regla 3: Notas bajas
            if grade < 5: score += 20
            # Regla 4: Poca participacion
            if posts < 2: score += 10

            level = "BAJO"
            if score >= 70: level = "CRITICO"
            elif score >= 40: level = "MEDIO"

            results.append({
                "student_id": student_id,
                "risk_score": score,
                "risk_level": level,
                "action_needed": level != "BAJO"
            })
        
        return pd.DataFrame(results)
