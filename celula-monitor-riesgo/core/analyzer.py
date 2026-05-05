# analyzer.py - Logica de deteccion de riesgo de abandono
# -------------------------------------------------------------------------
import pandas as pd
import os

class RiskAnalyzer:
    def __init__(self, data_path: str):
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"No se encuentra el archivo de datos: {data_path}")
        self.df = pd.read_csv(data_path)

    def calculate_risk(self):
        """
        Calcula el nivel de riesgo basado en reglas heuristicas.
        """
        results = []
        for _, row in self.df.iterrows():
            score = 0
            # Regla 1: Inactividad
            if row['last_login_days'] > 7: score += 40
            # Regla 2: Baja tasa de entrega
            if row['submission_rate'] < 0.5: score += 30
            # Regla 3: Notas bajas
            if row['avg_grade'] < 5: score += 20
            # Regla 4: Poca participacion
            if row['forum_posts'] < 2: score += 10

            level = "BAJO"
            if score >= 70: level = "CRITICO"
            elif score >= 40: level = "MEDIO"

            results.append({
                "student_id": row['student_id'],
                "risk_score": score,
                "risk_level": level,
                "action_needed": level != "BAJO"
            })
        
        return pd.DataFrame(results)

if __name__ == "__main__":
    # Test interno
    print("RiskAnalyzer cargado.")
