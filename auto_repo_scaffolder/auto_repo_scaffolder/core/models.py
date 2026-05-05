from pydantic import BaseModel, Field
from typing import List, Optional

class RepoConfig(BaseModel):
    """Entidad que define la configuración de un nuevo repositorio."""
    project_name: str = Field(..., min_length=3, description="Nombre del proyecto en snake_case")
    author: str = Field("Antigravity Célula Docensas", description="Autor del proyecto")
    description: str = Field(..., description="Breve descripción del propósito del proyecto")
    modules: List[str] = Field(default_factory=lambda: ["core", "adapters", "api"], description="Submódulos iniciales")
    include_tests: bool = True
