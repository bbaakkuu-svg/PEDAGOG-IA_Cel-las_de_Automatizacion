import http.server
import socketserver
import webbrowser
import os
import json
import threading

PORT = 8000
DIRECTORY = "web"
DATA_FILE = "data/competencias.json"

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path == '/api/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            try:
                with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), DATA_FILE), 'r', encoding='utf-8') as f:
                    self.wfile.write(f.read().encode())
            except FileNotFoundError:
                # Fallback genérico si falla
                self.wfile.write(json.dumps({"error": "No data found"}).encode())
        else:
            super().do_GET()

def _ensure_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    data_path = os.path.join(base_dir, DATA_FILE)
    if not os.path.exists(data_path):
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
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(mock_data, f, indent=4)

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
