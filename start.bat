@echo off
echo.
echo ========================================
echo   Maps4Study - Iniciando Servidor...
echo ========================================
echo.

:: Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python não está instalado ou não está no PATH.
    echo Instale Python em: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Verifica se as dependências estão instaladas
python -c "import flask; import requests; import duckduckgo_search" >nul 2>&1
if errorlevel 1 (
    echo [AVISO] Dependências faltando. Instalando...
    pip install flask requests duckduckgo-search
    if errorlevel 1 (
        echo [ERRO] Falha ao instalar dependências.
        pause
        exit /b 1
    )
)

:: Verifica se o build do React existe
if not exist "dist\index.html" (
    echo [ERRO] O build React não foi encontrado em dist/index.html
    echo Execute: npm run build
    pause
    exit /b 1
)

:: Inicia o servidor
echo [OK] Iniciando servidor Flask em http://localhost:5000
echo.
echo Pressione CTRL+C para parar o servidor.
echo.
python appduck.py

pause
