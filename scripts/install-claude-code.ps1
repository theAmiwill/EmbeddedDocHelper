param(
  [string]$SourceRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path,
  [string]$Destination = (Join-Path $HOME '.claude\skills')
)

$ErrorActionPreference = 'Stop'
$skills = @('vehicle-embedded-doc-indexer', 'vehicle-embedded-doc-curator')
New-Item -ItemType Directory -Force $Destination | Out-Null

foreach ($skill in $skills) {
  $source = Join-Path $SourceRoot "skills\$skill"
  if (-not (Test-Path $source)) {
    throw "Missing skill source: $source"
  }
  Copy-Item -Path $source -Destination $Destination -Recurse -Force
  Write-Host "Installed $skill -> $Destination"
}
