import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from rich.logging import RichHandler

def setup_logger(name: str):
    """
    Configura un logger industrial con salida a consola (Rich) y archivo rotativo.
    """
    # Determinar ruta de logs en la raíz del proyecto
    root_dir = Path(__file__).parent.parent
    log_dir = root_dir / "logs"
    if not log_dir.exists():
        log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / f"{name}.log"

    # Logger principal
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Handler para Consola (Rich)
    console_handler = RichHandler(rich_tracebacks=True, markup=True)
    console_handler.setLevel(logging.INFO)

    # Handler para Archivo (Rotativo)
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    
    # Formato para archivo
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)

    # Evitar duplicados si se llama varias veces
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger

# Instancia por defecto
logger = setup_logger("PEDAGOG-IA")
