import os
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta

class FileCache:
    """Sistema de caché simple basado en archivos para el ecosistema PEDAGOG-IA."""
    
    def __init__(self, cache_name="default", ttl_days=7):
        root_dir = Path(__file__).parent.parent
        self.cache_dir = root_dir / ".cache" / cache_name
        self.ttl = timedelta(days=ttl_days)
        
        if not self.cache_dir.exists():
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_hash(self, key_content: str) -> str:
        return hashlib.sha256(key_content.encode('utf-8')).hexdigest()

    def get(self, key_content: str):
        """Recupera un valor de la caché si existe y no ha expirado."""
        cache_key = self._get_hash(key_content)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Verificar expiración
                timestamp = datetime.fromisoformat(data['timestamp'])
                if datetime.now() - timestamp < self.ttl:
                    return data['content']
                else:
                    os.remove(cache_file) # Limpiar expirado
            except Exception:
                return None
        return None

    def set(self, key_content: str, value):
        """Guarda un valor en la caché."""
        cache_key = self._get_hash(key_content)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        data = {
            "timestamp": datetime.now().isoformat(),
            "content": value
        }
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception:
            return False

# Instancia global para fácil acceso
default_cache = FileCache()
