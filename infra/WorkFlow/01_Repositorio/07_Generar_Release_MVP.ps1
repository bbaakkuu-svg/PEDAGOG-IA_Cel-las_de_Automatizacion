# 07_Generar_Release_MVP.ps1
# Generacion de ejecutable autocontenido para el Auditor de Rubricas
# -------------------------------------------------------------------------
. "$PSScriptRoot\..\00_Core_Loader.ps1"

Write-WFLog "--- INICIANDO PROCESO DE RELEASE: AUDITOR DE RUBRICAS MVP ---" "Cyan"

# 1. Asegurar PyInstaller
Write-WFLog "Instalando PyInstaller..." "Gray"
python -m pip install pyinstaller --quiet

# 2. Preparar Directorio de Release
$releaseDir = Join-Path (Get-Location) "Release"
if (!(Test-Path $releaseDir)) { New-Item -ItemType Directory -Path $releaseDir }

# 3. Compilar el Ejecutable
# Usamos --paths para incluir las carpetas de infraestructura en el build
$auditorPath = "celula-auditor-rubricas"
Write-WFLog "Compilando ejecutable (esto puede tardar unos minutos)..." "White"

# Definimos las rutas a incluir
$infraPaths = "api_intelligence_wrapper,auto_repo_scaffolder,cloud_native_task_scheduler,ecosystem_sync_orchestrator"

# Ejecutamos PyInstaller
# --onefile: Un solo archivo .exe
# --name: Nombre del ejecutable
# --distpath: Carpeta de salida
python -m PyInstaller --onefile `
    --name "Auditor_Rubricas_MVP" `
    --distpath $releaseDir `
    --workpath (Join-Path $releaseDir "build") `
    --specpath $releaseDir `
    --paths "." `
    --collect-all "api_intelligence_wrapper" `
    (Join-Path $auditorPath "main.py")

if ($LASTEXITCODE -eq 0) {
    Write-WFLog "¡Release generada con exito!" "Green"
    Write-WFLog "Ubicacion: $releaseDir\Auditor_Rubricas_MVP.exe" "Cyan"
} else {
    Write-WFLog "Error durante la compilacion." "Red"
}
