import http.server
import socketserver
import webbrowser
import os
import json
import threading

PORT = 8000
# Resolución de directorios para PyInstaller
if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

DIRECTORY = os.path.join(base_dir, "web")
DATA_FILE = os.path.join(base_dir, "data", "competencias.json")

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path == '/api/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    self.wfile.write(f.read().encode())
            except FileNotFoundError:
                # Fallback genérico si falla
                self.wfile.write(json.dumps({"error": "No data found"}).encode())
        else:
            super().do_GET()

def _ensure_data():
    data_dir = os.path.join(base_dir, "data")
    if not os.path.exists(data_dir):
        try:
            os.makedirs(data_dir)
        except OSError:
            pass # Silencioso si ocurre un error de permisos en tmp
    
    if not os.path.exists(DATA_FILE):
        # Datos iniciales para la industrialización
        mock_data = {
            "student_name": "Ana Rodriguez",
            "course": "Máster en Automatización Industrial",
            "competencies": [
                {"name": "Pensamiento Computacional", "value": 90, "average": 70},
                {"name": "Arquitectura Limpia", "value": 85, "average": 65},
                {"name": "Resolución de Problemas", "value": 95, "average": 75},
                {"name": "Integración de IA", "value": 88, "average": 60},
                {"name": "Trabajo en Equipo", "value": 75, "average": 80}
            ],
            "ai_insight": "Ana muestra un dominio excepcional en habilidades técnicas (Arquitectura e IA). Se sugiere fomentar el liderazgo en proyectos colaborativos."
        }
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(mock_data, f, indent=4)
        except OSError:
            pass # Si no hay permisos de escritura, no podemos guardarlo, usaremos el mock

def run_dashboard():
    _ensure_data()
    print(f"🚀 Iniciando Dashboard de Competencias en http://localhost:{PORT}")
    
    def open_browser():
        webbrowser.open(f"http://localhost:{PORT}")
        
    # Abrir navegador en un hilo para no bloquear el servidor
    threading.Timer(1.0, open_browser).start()
    
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nDashboard detenido.")
            httpd.shutdown()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    run_dashboard()
