# 03_Auto_Branch_Commits.ps1
# Automatizacion masiva de Ramas y Commits para PEDAGOG-IA
# -------------------------------------------------------------------------
. "$PSScriptRoot\00_Core_Loader.ps1"

$tasks = @(
    @{id=1; slug="infra-tablero"; msg="feat: initialize docs and global requirements (close #1)"; files=@(@{path="docs/blueprint.md"; content="# Pedagogical Blueprint\nBase de la arquitectura de la celula."}, @{path="requirements.txt"; content="pydantic\njinja2\nrich\ngh-cli"})}
    @{id=2; slug="scaffolder-pydantic"; msg="feat: implement pydantic models for repo config (close #2)"; files=@(@{path="auto_repo_scaffolder/models/config.py"; content="from pydantic import BaseModel\n\nclass RepoConfig(BaseModel):\n    name: str\n    owner: str"})}
    @{id=3; slug="scaffolder-jinja2"; msg="feat: add jinja2 engine and fs adapter (close #3)"; files=@(@{path="auto_repo_scaffolder/engine/generator.py"; content="import jinja2\n\nclass ScaffolderEngine:\n    pass"})}
    @{id=4; slug="api-intelligence"; msg="feat: develop api intelligence wrapper client (close #4)"; files=@(@{path="api_intelligence_wrapper/client.py"; content="class AIClient:\n    def query(self, prompt: str):\n        pass"})}
    @{id=5; slug="ecosystem-orchestrator"; msg="feat: implementation of sync orchestrator (close #5)"; files=@(@{path="ecosystem_sync_orchestrator/sync.py"; content="class SyncOrchestrator:\n    def sync_all(self):\n        pass"})}
    @{id=6; slug="cloud-scheduler"; msg="feat: configure cloud native task scheduler (close #6)"; files=@(@{path="cloud_native_task_scheduler/scheduler.py"; content="class TaskScheduler:\n    def schedule(self):\n        pass"})}
)

foreach ($task in $tasks) {
    $branchName = "feature/issue-$($task.id)-$($task.slug)"
    Write-WFLog "--- PROCESANDO TAREA $($task.id): $($task.slug) ---" "Cyan"
    
    # 1. Crear y cambiar a la rama
    git checkout -b $branchName
    
    # 2. Crear archivos
    foreach ($file in $task.files) {
        $dir = [System.IO.Path]::GetDirectoryName($file.path)
        if ($dir -and !(Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force }
        $file.content | Out-File $file.path -Encoding utf8
    }
    
    # 3. Commit
    git add .
    git commit -m $task.msg
    
    # 4. Push (opcional, lo habilitamos)
    git push origin $branchName
    
    # 5. Volver a develop
    git checkout develop
}

Write-WFLog "¡Todas las ramas y commits han sido procesados con exito!" "Green"
