import http.server
import socketserver
import webbrowser
import os
import json
import sys
import threading
from pathlib import Path

# Forzar codificación UTF-8 en Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Resolución de rutas para acceder al núcleo compartido y a la infra
root_path = Path(__file__).parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

# Inyectar el path del dashboard para importar su core
dashboard_path = Path(__file__).parent
if str(dashboard_path) not in sys.path:
    sys.path.insert(0, str(dashboard_path))

try:
    from dashboard_core.data_engine import DataEngine
except ImportError as e:
    print(f"Error cargando DataEngine: {e}")
    sys.exit(1)

PORT = 8000
DIRECTORY = os.path.join(dashboard_path, "web")
data_engine = DataEngine(root_path)

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path == '/api/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            data = data_engine.get_dashboard_data()
            self.wfile.write(json.dumps(data).encode('utf-8'))
        else:
            super().do_GET()

def run_dashboard():
    print(f"🚀 Iniciando Command Center PEDAGOG-IA en http://localhost:{PORT}")
    
    def open_browser():
        webbrowser.open(f"http://localhost:{PORT}")
        
    threading.Timer(1.5, open_browser).start()
    
    # Permitir reutilización de puerto
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nDashboard detenido.")
            httpd.shutdown()

if __name__ == "__main__":
    # Asegurar que estamos en el directorio correcto para servir archivos
    os.chdir(dashboard_path)
    run_dashboard()
