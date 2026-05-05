import pytest
from pathlib import Path
from auto_repo_scaffolder.core.models import RepoConfig
from auto_repo_scaffolder.core.scaffolder import RepoScaffolder, FileSystemAdapter

def test_scaffolder_creates_project_structure(tmp_path):
    # Setup
    config = RepoConfig(
        project_name="test_project",
        description="A test project"
    )
    scaffolder = RepoScaffolder(FileSystemAdapter())
    
    # Execute
    scaffolder.execute(config, tmp_path)
    
    # Assert
    assert (tmp_path / "test_project").exists()
    assert (tmp_path / "test_project" / "setup.py").exists()
    assert (tmp_path / "test_project" / "test_project" / "core" / "__init__.py").exists()
    assert (tmp_path / "test_project" / "tests" / "__init__.py").exists()
