param(
  [Parameter(Mandatory = $true)]
  [string]$TargetProject,
  [string]$SourceRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
)

$ErrorActionPreference = 'Stop'
$target = Resolve-Path $TargetProject
$githubDir = Join-Path $target '.github'
$instructionsDir = Join-Path $githubDir 'instructions'
$repoInstructions = Join-Path $githubDir 'copilot-instructions.md'
$pathInstructions = Join-Path $instructionsDir 'embedded-doc-helper.instructions.md'
$templateRoot = Join-Path $SourceRoot 'install\github-copilot'

New-Item -ItemType Directory -Force $githubDir | Out-Null
New-Item -ItemType Directory -Force $instructionsDir | Out-Null

$section = Get-Content -Raw (Join-Path $templateRoot 'copilot-instructions.md')
$markerStart = '<!-- EmbeddedDocHelper start -->'
$markerEnd = '<!-- EmbeddedDocHelper end -->'
$markedSection = "$markerStart`n$section`n$markerEnd`n"

if (Test-Path $repoInstructions) {
  $existing = Get-Content -Raw $repoInstructions
  if ($existing -notlike "*$markerStart*") {
    $prefix = if ($existing.EndsWith("`n")) { '' } else { "`n" }
    Set-Content -Path $repoInstructions -Value ($existing + $prefix + "`n" + $markedSection) -Encoding UTF8
    Write-Host "Appended EmbeddedDocHelper section -> $repoInstructions"
  } else {
    Write-Host "EmbeddedDocHelper section already present -> $repoInstructions"
  }
} else {
  Set-Content -Path $repoInstructions -Value $markedSection -Encoding UTF8
  Write-Host "Created $repoInstructions"
}

Copy-Item -Path (Join-Path $templateRoot 'embedded-doc-helper.instructions.md') -Destination $pathInstructions -Force
Write-Host "Installed path-specific instructions -> $pathInstructions"
