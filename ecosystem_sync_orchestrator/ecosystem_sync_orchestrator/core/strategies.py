from abc import ABC, abstractmethod

class SyncStrategy(ABC):
    """Contrato para estrategias de sincronización."""
    
    @abstractmethod
    def sync_project(self, project_path: str, message: str):
        """Ejecuta la sincronización de un proyecto específico."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass
