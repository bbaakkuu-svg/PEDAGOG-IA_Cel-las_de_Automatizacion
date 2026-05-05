# 08_Publicar_Release.ps1
# Automatiza el proceso de versionado y lanzamiento de una nueva release (Refactorizado)
. "$PSScriptRoot\00_Core_Loader.ps1"

$version = Read-Host "Cual es el numero de la nueva version? (ej: 1.4)"
if (!$version) { Write-WFLog "Operacion cancelada." "Red"; exit }

$tagName = "v$version"
$fullRepo = "$Global:REPO_OWNER/$Global:REPO_NAME"

Write-WFLog "--- INICIANDO PROCESO DE RELEASE $tagName ---"

# 1. Actualizar pom.xml (Maven) - Busqueda dinamica del archivo
$pomPath = Join-Path (Get-Location) "pom.xml"
if (Test-Path $pomPath) {
    Write-WFLog "Actualizando version en pom.xml..."
    (Get-Content $pomPath) -replace '<version>.*</version>', "<version>$version</version>" | Set-Content $pomPath
}

# 2. Git Workflow
Write-WFLog "Preparando tags y commits..."
git add .
git commit -m "chore: release $tagName para $($WFConfig.project.name)"
git tag -a $tagName -m "Release $tagName"

Write-WFLog "Sincronizando con $Global:BRANCH_MAIN..."
git checkout $Global:BRANCH_MAIN
git merge $Global:BRANCH_DEV
git push origin $Global:BRANCH_MAIN $Global:BRANCH_DEV --tags

# 3. GitHub Release
Write-WFLog "Creando Release en GitHub..." "Yellow"
$notas = "NutriPlan Pro $tagName - Nueva versión del Framework de automatización integrada."
gh release create $tagName --title "$($WFConfig.project.name) $tagName" --notes $notas

Write-WFLog "Version $tagName publicada con exito!" "Green"
