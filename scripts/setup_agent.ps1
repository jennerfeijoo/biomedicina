param(
    [switch]$PullModels
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

foreach ($command in @("python", "ollama", "git", "gh")) {
    if (-not (Get-Command $command -ErrorAction SilentlyContinue)) {
        throw "No se encontró '$command' en PATH. Instálalo antes de continuar."
    }
}

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

$Python = Join-Path $Root ".venv\Scripts\python.exe"
& $Python -m pip install --upgrade pip
& $Python -m pip install -r requirements-agent.txt

if ($PullModels) {
    foreach ($model in @("qwen3.6:27b", "ornith:9b", "qwen3-embedding:0.6b")) {
        ollama pull $model
    }
}

try {
    gh auth status | Out-Host
}
catch {
    Write-Host "GitHub CLI todavía no está autenticado. Ejecuta: gh auth login" -ForegroundColor Yellow
    exit 1
}

& $Python scripts/run_citonauta_agent.py preflight
Write-Host "Configuración del agente completada." -ForegroundColor Green
