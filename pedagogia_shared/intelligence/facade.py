from typing import List
from .models import PedagogiaAsset

class PedagogiaAPIClient:
    """Simulación de un cliente de API de bajo nivel con complejidad."""
    def get_raw_data(self, token: str):
        # Respuesta JSON simulada
        return [
            {"id": "101", "display_name": "Curso Clean Architecture", "category": "Technical", "last_updated": "2024-05-01T10:00:00Z", "status": "active"},
            {"id": "102", "display_name": "Taller Pydantic", "category": "DevOps", "last_updated": "2024-05-02T12:00:00Z", "status": "pending"}
        ]

class PedagogiaIntelligenceFacade:
    """La Facade: El punto de entrada simplificado a la IA."""
    
    def __init__(self, api_token: str):
        self._client = PedagogiaAPIClient()
        self._token = api_token

    def fetch_active_assets(self) -> List[PedagogiaAsset]:
        """Fetch y filtrado de activos activos."""
        raw_data = self._client.get_raw_data(self._token)
        assets = [PedagogiaAsset(**item) for item in raw_data]
        return [a for a in assets if a.status == "active"]

    def generate_summary(self, text: str) -> str:
        """Simulación de generación de resumen por LLM."""
        return f"RESUMEN EJECUTIVO (AI):\nEl contenido trata sobre {text[:100]}...\n\nImpacto Pedagógico: Alto."

    def generate_quiz(self, text: str) -> List[dict]:
        """Simulación de generación de cuestionario por LLM."""
        return [
            {
                "question": "¿Cuál es el concepto clave del texto?",
                "options": ["Opción A", "Opción B", "Opción C", "Opción D"],
                "answer": "Opción A"
            }
        ]
