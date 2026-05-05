from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional

class DocensaAsset(BaseModel):
    """Modelo de datos unificado para un activo de Docensas."""
    id: str
    title: str = Field(..., alias="display_name")
    category: str
    last_updated: datetime
    status: str = "active"

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        if v not in ["active", "archived", "pending"]:
            raise ValueError("Estado no válido")
        return v
