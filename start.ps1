# PowerShell script to start Maps4Study server

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Maps4Study - Iniciando Servidor..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verifica Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERRO] Python não está instalado ou não está no PATH." -ForegroundColor Red
    Write-Host "Instale em: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Verifica dependências
Write-Host "[...] Verificando dependências..." -ForegroundColor Yellow
try {
    python -c "import flask; import requests; import duckduckgo_search" 2>&1 | Out-Null
    Write-Host "[OK] Dependências instaladas" -ForegroundColor Green
} catch {
    Write-Host "[AVISO] Instalando dependências..." -ForegroundColor Yellow
    pip install flask requests duckduckgo-search
}

# Verifica build React
if (-not (Test-Path "dist\index.html")) {
    Write-Host "[ERRO] Build React não encontrado em dist/index.html" -ForegroundColor Red
    Write-Host "Execute: npm run build" -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host "[OK] Build React encontrado" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Iniciando servidor Flask..." -ForegroundColor Green
Write-Host "📍 Acesse: http://localhost:5000" -ForegroundColor Cyan
Write-Host "🛑 Pressione CTRL+C para parar" -ForegroundColor Yellow
Write-Host ""

python appduck.py
