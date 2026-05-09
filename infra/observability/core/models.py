from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum

class InteractionStatus(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    TIMEOUT = "timeout"

class IAInteraction(BaseModel):
    interaction_id: str = Field(..., description="UUID unico de la interaccion")
    timestamp: datetime = Field(default_factory=datetime.now)
    cell_id: str = Field(..., description="ID de la celula que realiza la peticion (ej: auditor)")
    model_id: str = Field(..., description="ID del modelo utilizado (ej: gemini-1.5-pro)")
    
    # Metricas de Rendimiento
    latency_ms: float = Field(..., description="Tiempo de respuesta en milisegundos")
    status: InteractionStatus = Field(default=InteractionStatus.SUCCESS)
    error_message: Optional[str] = None
    
    # Metricas de Coste (Tokens)
    prompt_tokens: int = Field(default=0)
    completion_tokens: int = Field(default=0)
    total_tokens: int = Field(default=0)
    
    # Metadatos Adicionales
    metadata: Dict[str, Any] = Field(default_factory=dict)

class CostConfig(BaseModel):
    model_name: str
    input_cost_per_1k: float
    output_cost_per_1k: float
