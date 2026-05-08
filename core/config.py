
import os
from pathlib import Path
from dotenv import load_dotenv

# Encontrar la raíz del proyecto (donde está el .env)
ROOT_DIR = Path(__file__).parent.parent
env_path = ROOT_DIR / ".env"

# Cargar variables de entorno
load_dotenv(dotenv_path=env_path)

class Config:
    """Acceso centralizado a la configuración del ecosistema."""
    
    # Tokens
    PEDAGOGIA_API_TOKEN = os.getenv("PEDAGOGIA_API_TOKEN", "DEV_TOKEN_UNSET")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Flags
    DEBUG = os.getenv("DEBUG_MODE", "True").lower() in ("true", "1", "yes")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Paths base
    PROJECT_ROOT = ROOT_DIR
    
    @classmethod
    def validate(cls):
        """Valida que las variables críticas estén presentes."""
        critical_vars = ["PEDAGOGIA_API_TOKEN"]
        missing = [v for v in critical_vars if getattr(cls, v) == "DEV_TOKEN_UNSET"]
        return missing

if __name__ == "__main__":
    print(f"Project Root: {Config.PROJECT_ROOT}")
    print(f"Debug Mode: {Config.DEBUG}")
    print(f"API Token: {Config.PEDAGOGIA_API_TOKEN}")
