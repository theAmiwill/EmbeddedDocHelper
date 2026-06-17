param(
  [Parameter(Mandatory = $true)]
  [ValidateSet('codex', 'claude-code', 'kilo-code')]
  [string]$Agent,
  [Parameter(Mandatory = $true)]
  [string]$TargetProject,
  [string]$SourceRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
)

$ErrorActionPreference = 'Stop'

function Get-TemplateText {
  $path = Join-Path $SourceRoot 'install\agent-rules\embedded-doc-helper.md'
  if (-not (Test-Path $path)) {
    throw "Missing rules template: $path"
  }
  return Get-Content -Raw $path
}

function Add-MarkedSection {
  param(
    [string]$Path,
    [string]$Content
  )

  $markerStart = '<!-- EmbeddedDocHelper start -->'
  $markerEnd = '<!-- EmbeddedDocHelper end -->'
  $markedSection = "$markerStart`n$Content`n$markerEnd`n"

  $parent = Split-Path -Parent $Path
  if ($parent) {
    New-Item -ItemType Directory -Force $parent | Out-Null
  }

  if (Test-Path $Path) {
    $existing = Get-Content -Raw $Path
    if ($existing -like "*$markerStart*") {
      Write-Host "EmbeddedDocHelper section already present -> $Path"
      return
    }
    $prefix = if ($existing.EndsWith("`n")) { '' } else { "`n" }
    Set-Content -Path $Path -Value ($existing + $prefix + "`n" + $markedSection) -Encoding UTF8
    Write-Host "Appended EmbeddedDocHelper rules -> $Path"
    return
  }

  Set-Content -Path $Path -Value $markedSection -Encoding UTF8
  Write-Host "Created EmbeddedDocHelper rules -> $Path"
}

$target = (Resolve-Path $TargetProject).Path
$content = Get-TemplateText

switch ($Agent) {
  'codex' {
    Add-MarkedSection -Path (Join-Path $target 'AGENTS.md') -Content $content
  }
  'claude-code' {
    Add-MarkedSection -Path (Join-Path $target 'CLAUDE.md') -Content $content
  }
  'kilo-code' {
    Add-MarkedSection -Path (Join-Path $target '.kilocode\rules\embedded-doc-helper.md') -Content $content
  }
}
