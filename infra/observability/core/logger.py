import json
import os
from datetime import datetime
from uuid import uuid4
from typing import Optional, Dict, Any
from .models import IAInteraction, InteractionStatus

class TelemetryLogger:
    def __init__(self, log_dir: str = "data/logs/observability"):
        self.log_dir = log_dir
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir, exist_ok=True)
            
    def log_interaction(
        self,
        cell_id: str,
        model_id: str,
        latency_ms: float,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        status: InteractionStatus = InteractionStatus.SUCCESS,
        error_message: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        interaction_id = str(uuid4())
        
        interaction = IAInteraction(
            interaction_id=interaction_id,
            cell_id=cell_id,
            model_id=model_id,
            latency_ms=latency_ms,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
            status=status,
            error_message=error_message,
            metadata=metadata or {}
        )
        
        self._persist(interaction)
        return interaction_id

    def _persist(self, interaction: IAInteraction):
        # Persistencia en JSON diario para facilitar el analisis
        date_str = datetime.now().strftime("%Y-%m-%d")
        file_path = os.path.join(self.log_dir, f"ia_ops_{date_str}.jsonl")
        
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(interaction.model_dump_json() + "\n")

# Instancia global para facilitar la importacion
default_logger = TelemetryLogger()
