from abc import ABC, abstractmethod

class TaskExecutor(ABC):
    """Interfaz abstracta que define el contrato de ejecución."""
    
    @abstractmethod
    def run(self, task_name: str, payload: dict):
        """Ejecuta una tarea específica."""
        pass

    @property
    @abstractmethod
    def environment(self) -> str:
        """Devuelve el nombre del entorno de ejecución."""
        pass
