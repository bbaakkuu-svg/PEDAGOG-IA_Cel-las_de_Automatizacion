# main.py - Launcher del Dashboard de Competencias
# -------------------------------------------------------------------------
import http.server
import socketserver
import webbrowser
import os

PORT = 8000
DIRECTORY = "web"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def run_dashboard():
    print(f"🚀 Iniciando Dashboard en http://localhost:{PORT}")
    webbrowser.open(f"http://localhost:{PORT}")
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nDashboard detenido.")
            httpd.shutdown()

if __name__ == "__main__":
    # Asegurarse de estar en el directorio correcto
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    run_dashboard()
