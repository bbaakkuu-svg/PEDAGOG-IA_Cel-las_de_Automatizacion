import sys
import os
import argparse
from pathlib import Path

# Forzar codificación UTF-8 en Windows para evitar errores con emojis
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Configuración de rutas
root_path = Path(__file__).parent
sys.path.insert(0, str(root_path))

from infra.ecosystem_sync_orchestrator.pedagogical_brain import PedagogicalBrain

def main():
    parser = argparse.ArgumentParser(description="PEDAGOG-IA Orchestrator: El Cerebro Central")
    parser.add_argument("command", choices=["evaluate", "reinforce", "full-cycle"], help="Comando a ejecutar")
    parser.add_argument("--file", help="Archivo a procesar")
    parser.add_argument("--student", help="ID del estudiante")
    
    args = parser.parse_args()
    brain = PedagogicalBrain()

    if args.command == "evaluate":
        # Ejecuta el auditor
        print(f"[*] Lanzando Auditor para: {args.file}")
        os.system(f"python cells/auditor/main.py {args.file}")
        
    elif args.command == "reinforce":
        # Ejecuta el refuerzo basado en el último JSON de evaluación
        eval_path = os.path.join(root_path, "output", "evaluations", f"{os.path.splitext(os.path.basename(args.file))[0]}.json")
        if os.path.exists(eval_path):
            brain.run_full_cycle(eval_path)
        else:
            print(f"[!] Error: No se encontró evaluación previa en {eval_path}")

    elif args.command == "full-cycle":
        print("[⚡] INICIANDO CICLO PEDAGÓGICO COMPLETO")
        # 1. Evaluar
        os.system(f"python cells/auditor/main.py {args.file}")
        # 2. Reforzar
        eval_name = os.path.splitext(os.path.basename(args.file))[0]
        eval_path = os.path.join(root_path, "output", "evaluations", f"{eval_name}.json")
        if os.path.exists(eval_path):
            print("\n[🧠] CEREBRO CENTRAL: Analizando resultados para generar refuerzo...")
            brain.run_full_cycle(eval_path)
        print("[✅] CICLO COMPLETADO")

if __name__ == "__main__":
    main()
