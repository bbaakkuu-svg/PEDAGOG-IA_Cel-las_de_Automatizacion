import os
import sys
import json
from pathlib import Path

# Configuración de rutas para importar desde infra y core
root_path = Path(__file__).parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

try:
    from core.config import Config
    from infra.observability import default_logger, InteractionStatus
except ImportError:
    Config = None
    default_logger = None

# Inyección robusta del motor del Generador (evitando colisión con root/core)
import importlib.util
gen_engine_path = os.path.join(root_path, "cells", "generator", "core", "engine.py")

ContentEngine = None
if os.path.exists(gen_engine_path):
    try:
        # Añadir el directorio del generador al path para sus propias importaciones internas
        gen_dir = os.path.dirname(os.path.dirname(gen_engine_path))
        if gen_dir not in sys.path:
            sys.path.insert(0, gen_dir)
            
        spec = importlib.util.spec_from_file_location("generator_engine", gen_engine_path)
        gen_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gen_mod)
        ContentEngine = gen_mod.ContentEngine
    except Exception as e:
        print(f"[Brain] Error cargando el motor de generación: {e}")

class PedagogicalBrain:
    """El 'Cerebro Central' que orquestra la integración entre el Auditor y el Generador."""
    
    def __init__(self):
        self.last_results = None
        self.output_base = os.path.join(root_path, "output", "reinforcement")
        os.makedirs(self.output_base, exist_ok=True)
        
        # Inicializar el motor del generador si está disponible
        api_token = Config.PEDAGOGIA_API_TOKEN if Config else "DEV_TOKEN"
        self.gen_engine = ContentEngine(api_token=api_token) if ContentEngine else None

    def analyze_evaluation(self, evaluation_data: dict):
        """Analiza los resultados del Auditor para encontrar debilidades."""
        print(f"[Brain] Analizando evaluación de: {evaluation_data.get('source_file', 'Unknown')}")
        
        low_criteria = []
        for detail in evaluation_data.get('detalles', []):
            if detail.get('puntos', 10) < 6:
                low_criteria.append(detail['criterio'])
        
        return low_criteria

    def trigger_reinforcement(self, student_id: str, weaknesses: list):
        """Activa el Generador para crear material de refuerzo basado en las debilidades."""
        if not weaknesses:
            print("[Brain] No se detectaron debilidades. ¡Excelente progreso!")
            return None

        print(f"[Brain] Detectadas {len(weaknesses)} debilidades para {student_id}. Generando refuerzo autónomo...")
        
        reinforcement_topics = ", ".join(weaknesses)
        input_text = f"Temas de refuerzo pedagógico: {reinforcement_topics}. " \
                     f"El estudiante necesita mejorar en estos criterios evaluados por el Auditor SEA."
        
        # Carpeta específica para el estudiante
        student_dir = os.path.join(self.output_base, student_id)
        os.makedirs(student_dir, exist_ok=True)
        
        results = {
            "student_id": student_id,
            "topics": weaknesses,
            "timestamp": os.path.getmtime(__file__), # Simplificación
            "material": {}
        }

        # Ejecución real del motor si está disponible
        if self.gen_engine:
            start_time = os.times().elapsed # Simplificación para latencia
            
            # Generar Contenido
            summary = self.gen_engine.generate_summary(input_text)
            quiz = self.gen_engine.generate_quiz(input_text)
            
            results["material"] = {
                "summary": summary,
                "quiz": quiz
            }
            
            # Guardar archivos de salida legibles
            with open(os.path.join(student_dir, "guia_estudio.txt"), "w", encoding="utf-8") as f:
                f.write(summary)
            
            with open(os.path.join(student_dir, "cuestionario_refuerzo.json"), "w", encoding="utf-8") as f:
                json.dump(quiz, f, indent=4, ensure_ascii=False)
                
            print(f"[Brain] ✅ Material generado exitosamente en: {student_dir}")
            
            # Registro en Telemetría (Real)
            if default_logger:
                default_logger.log_interaction(
                    cell_id="brain_orchestrator",
                    model_id="pedagogical-bridge-v1-autogen",
                    latency_ms=500.0, # Estimación
                    status=InteractionStatus.SUCCESS,
                    metadata={"student_id": student_id, "mode": "autonomous"}
                )
        else:
            print("[Brain] ⚠️ Motor de Generación no disponible. El plan queda pendiente.")
            results["message"] = "Plan de refuerzo pendiente de ejecución (Motor offline)."
            
        return results

    def run_full_cycle(self, auditor_output_path: str):
        """Ejecuta el ciclo completo: Leer Auditor -> Analizar -> Preparar Generador."""
        # En este MVP, simulamos la lectura del archivo de salida del Auditor
        with open(auditor_output_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        weaknesses = self.analyze_evaluation(data)
        plan = self.trigger_reinforcement(data.get("student_id", "STU-001"), weaknesses)
        
        if plan:
            # Guardar el plan de refuerzo
            plan_path = os.path.join(self.output_base, f"plan_{data.get('student_id', 'STU-001')}.json")
            with open(plan_path, "w", encoding="utf-8") as f:
                json.dump(plan, f, indent=4)
            print(f"[Brain] Plan de refuerzo guardado en: {plan_path}")
            return plan
        return None

if __name__ == "__main__":
    # Script de prueba
    brain = PedagogicalBrain()
    # Simulamos un resultado del auditor
    mock_eval = {
        "student_id": "ALUMNO_PROTOTIPO",
        "source_file": "examen_ia.pdf",
        "nota": 5.5,
        "detalles": [
            {"criterio": "Arquitectura de Redes", "puntos": 4, "feedback": "Insuficiente"},
            {"criterio": "Programación Python", "puntos": 9, "feedback": "Excelente"}
        ]
    }
    
    # Crear archivo temporal para el test
    temp_path = "scratch/temp_eval.json"
    os.makedirs("scratch", exist_ok=True)
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(mock_eval, f)
        
    brain.run_full_cycle(temp_path)
