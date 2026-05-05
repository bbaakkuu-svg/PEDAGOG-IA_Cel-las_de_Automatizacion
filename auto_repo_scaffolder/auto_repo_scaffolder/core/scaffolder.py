import os
from pathlib import Path
from ..core.models import RepoConfig

class FileSystemAdapter:
    """Adaptador para interactuar con el sistema de archivos."""
    
    @staticmethod
    def create_directory(path: Path):
        path.mkdir(parents=True, exist_ok=True)
        
    @staticmethod
    def create_file(path: Path, content: str = ""):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

class RepoScaffolder:
    """Caso de Uso: Orquestar la creación del repositorio."""
    
    def __init__(self, adapter: FileSystemAdapter):
        self.adapter = adapter

    def execute(self, config: RepoConfig, base_path: Path):
        project_root = base_path / config.project_name
        module_root = project_root / config.project_name
        
        # 1. Crear estructura raíz
        dirs = [
            project_root,
            module_root,
            project_root / "tests",
            project_root / "docs",
        ]
        
        # 2. Crear submódulos definidos
        for module in config.modules:
            dirs.append(module_root / module)
            
        for d in dirs:
            self.adapter.create_directory(d)
            self.adapter.create_file(d / "__init__.py")

        # 3. Archivos base en la raíz
        self.adapter.create_file(project_root / "setup.py", "# Setup file auto-generated")
        self.adapter.create_file(project_root / "requirements.txt", "# Dependencies")
        self.adapter.create_file(project_root / "README.md", f"# {config.project_name}\n\n{config.description}")
