# 06_Inicia_Fase_Pedagogica.ps1
# Inicializacion de las 4 nuevas celulas de alto valor pedagógico
# -------------------------------------------------------------------------
. "$PSScriptRoot\..\00_Core_Loader.ps1"

$repo = "$($WFConfig.project.owner)/$($WFConfig.project.repo_name)"
$projectId = "PVT_kwHODg_sXs4BWzNs" # ID largo del Proyecto #5

$celulas = @(
    @{title="[CELULA] Auditor de Rubricas (Meta-Evaluador)"; slug="auditor-rubricas"; desc="Sistema de correccion asistida por IA con justificacion de criterios."}
    @{title="[CELULA] Monitor de Alumnos en Riesgo (EWS)"; slug="monitor-riesgo"; desc="Deteccion proactiva de patrones de abandono mediante analisis de logs."}
    @{title="[CELULA] Generador Dinamico de Material (IA)"; slug="generador-material"; desc="Transformacion automatica de temarios en recursos multimedia."}
    @{title="[CELULA] Dashboard de Competencias"; slug="dashboard-competencias"; desc="Visualizacion interactiva del progreso competencial mediante radar charts."}
)

Write-WFLog "--- INICIANDO FASE 2: CELULAS PEDAGOGICAS ---" "Cyan"

foreach ($celula in $celulas) {
    Write-WFLog "Creando Carpeta y README para: $($celula.slug)..." "White"
    $path = Join-Path (Get-Location) "celula-$($celula.slug)"
    if (!(Test-Path $path)) { New-Item -ItemType Directory -Path $path -Force }
    
    $readmeContent = "# 🚀 $($celula.title)\n\n$($celula.desc)\n\n## 🛠️ Stack Tecnologico\n- Python / JS\n- LangChain / OpenAI API\n- Plotly / D3.js\n"
    $readmeContent | Out-File (Join-Path $path "README.md") -Encoding utf8
    
    Write-WFLog "Creando Issue en GitHub..." "Gray"
    $issueUrl = gh issue create --repo $repo --title $celula.title --body $celula.desc --label "enhancement"
    
    # Extraer ID de la issue del URL
    # Vinculamos al proyecto
    gh project item-add 5 --owner "@me" --url $issueUrl
}

Write-WFLog "Fase 2 inicializada con exito. Carpetas y tareas listas." "Green"
