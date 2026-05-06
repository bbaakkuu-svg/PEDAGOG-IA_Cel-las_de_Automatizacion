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

    def _load_data(self) -> pd.DataFrame:
        """Carga datos desde CSV o Excel."""
        ext = os.path.splitext(self.data_path)[1].lower()
        try:
            if ext == '.csv':
                return pd.read_csv(self.data_path)
            elif ext in ['.xlsx', '.xls']:
                return pd.read_excel(self.data_path)
            else:
                raise ValueError(f"Formato de archivo no soportado: {ext}. Use .csv o .xlsx")
        except Exception as e:
            raise RuntimeError(f"Error al leer el archivo {ext}: {e}")

    def calculate_risk(self):
        """
        Calcula el nivel de riesgo basado en reglas heuristicas.
        """
        if self.df.empty:
            return pd.DataFrame()

        results = []
        for _, row in self.df.iterrows():
            score = 0
            # Regla 1: Inactividad
            if row.get('last_login_days', 0) > 7: score += 40
            # Regla 2: Baja tasa de entrega
            if row.get('submission_rate', 1.0) < 0.5: score += 30
            # Regla 3: Notas bajas
            if row.get('avg_grade', 10.0) < 5: score += 20
            # Regla 4: Poca participacion
            if row.get('forum_posts', 5) < 2: score += 10

            level = "BAJO"
            if score >= 70: level = "CRITICO"
            elif score >= 40: level = "MEDIO"

            results.append({
                "student_id": row.get('student_id', 'N/A'),
                "risk_score": score,
                "risk_level": level,
                "action_needed": level != "BAJO"
            })
        
        return pd.DataFrame(results)
