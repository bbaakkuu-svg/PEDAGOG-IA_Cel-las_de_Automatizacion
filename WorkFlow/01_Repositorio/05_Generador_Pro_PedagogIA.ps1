# 05_Generador_Pro_PedagogIA.ps1
# Script especializado para la generacion de Issues del Proyecto PEDAGOG-IA
# -------------------------------------------------------------------------
. "$PSScriptRoot\..\00_Core_Loader.ps1"

$repo = "$($WFConfig.project.owner)/$($WFConfig.project.repo_name)"

$issues = @(
    @{
        title="[TASK] Infraestructura: Inicializacion de Tablero y Estandares"; 
        body="Configurar el Project v2 en GitHub y sincronizar las etiquetas personalizadas segun el WorkFlow Elite.";
        labels="enhancement,critical"
    },
    @{
        title="[TASK] Scaffolder: Implementacion de Capa de Validacion Pydantic"; 
        body="Desarrollar el esquema RepoConfig con tipado estricto para garantizar la consistencia de los nuevos repositorios.";
        labels="enhancement"
    },
    @{
        title="[TASK] Scaffolder: Motor de Plantillas Jinja2 y Adaptador FileSystem"; 
        body="Implementar la generacion fisica de la estructura Kenneth Reitz separando la logica de negocio de la infraestructura.";
        labels="enhancement"
    },
    @{
        title="[TASK] API Intel: Desarrollo del Wrapper de Inteligencia"; 
        body="Crear el modulo 'api_intelligence_wrapper' para centralizar las llamadas a modelos de IA y herramientas externas.";
        labels="enhancement"
    },
    @{
        title="[TASK] Orchestrator: Sincronizacion del Ecosistema"; 
        body="Desarrollar el 'ecosystem_sync_orchestrator' para mantener la integridad de todas las celulas de automatizacion.";
        labels="enhancement"
    },
    @{
        title="[TASK] Scheduler: Integracion de Tareas Cloud Native"; 
        body="Configurar el 'cloud_native_task_scheduler' para la ejecucion programada y escalable de los procesos de la celula.";
        labels="enhancement"
    },
    @{
        title="[TASK] Docs: Blueprint Pedagogico y READMEs Industriales"; 
        body="Finalizar la documentacion tecnica y pedagogica de cada modulo, asegurando un onboarding 'Senior-Ready'.";
        labels="documentation"
    }
)

Write-WFLog "--- CARGANDO ROADMAP PEDAGOG-IA EN GITHUB ---" "Cyan"

foreach ($issue in $issues) {
    Write-WFLog "Creando: $($issue.title)..." "White"
    gh issue create --repo $repo --title $issue.title --body $issue.body --label $issue.labels
}

Write-WFLog "¡Roadmap inyectado con exito en el repositorio!" "Green"
