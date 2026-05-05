from typing import List
from .core.models import DocensaAsset

class DocensasAPIClient:
    """Simulación de un cliente de API de bajo nivel con complejidad."""
    def get_raw_data(self, token: str):
        # Imagina una respuesta JSON cruda y desordenada
        return [
            {"id": "101", "display_name": "Curso Clean Architecture", "category": "Technical", "last_updated": "2024-05-01T10:00:00Z", "status": "active"},
            {"id": "102", "display_name": "Taller Pydantic", "category": "DevOps", "last_updated": "2024-05-02T12:00:00Z", "status": "pending"}
        ]

class DocensasIntelligenceFacade:
    """La Facade: El punto de entrada simplificado."""
    
    def __init__(self, api_token: str):
        self._client = DocensasAPIClient()
        self._token = api_token

    def fetch_active_assets(self) -> List[DocensaAsset]:
        """
        Punto de entrada único que maneja:
        1. Autenticación.
        2. Fetch de datos.
        3. Filtrado de lógica de negocio.
        4. Modelado y validación.
        """
        raw_data = self._client.get_raw_data(self._token)
        assets = [DocensaAsset(**item) for item in raw_data]
        return [a for a in assets if a.status == "active"]
