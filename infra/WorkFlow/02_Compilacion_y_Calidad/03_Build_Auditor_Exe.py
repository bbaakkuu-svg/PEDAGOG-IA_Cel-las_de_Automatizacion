import os
import subprocess
import sys
import io

# Forzar UTF-8 para evitar errores de charmap en Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def build():
    print("🚀 Iniciando compilación de Auditor de Rúbricas v2.0...")
    
    # Rutas
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    release_dir = os.path.join(root_dir, "Release")
    spec_file = os.path.join(release_dir, "Auditor_Rubricas_MVP.spec")
    
    if not os.path.exists(spec_file):
        print(f"Error: No se encontró el archivo .spec en {spec_file}")
        return

    # Comando de PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--workpath", os.path.join(release_dir, "build"),
        "--distpath", release_dir,
        spec_file
    ]
    
    try:
        print(f"Carpeta Release: {release_dir}")
        subprocess.run(cmd, check=True, cwd=root_dir)
        print("\n¡Éxito! El nuevo binario ADI v2.0 ha sido generado en la carpeta /Release.")
    except subprocess.CalledProcessError as e:
        print(f"\nError durante la compilación: {e}")
    except Exception as e:
        print(f"\nError inesperado: {e}")

if __name__ == "__main__":
    build()
