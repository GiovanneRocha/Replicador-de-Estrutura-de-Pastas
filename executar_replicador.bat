@echo off
chcp 65001 > nul
cd /d "%~dp0"
echo ==============================================
echo REPLICADOR DE ESTRUTURA DE PASTAS - COMPLETO
echo ==============================================
python replicador_estrutura.py
if %errorlevel% neq 0 (
    echo.
    echo O processo terminou com erro.
) else (
    echo.
    echo PROCESSO COMPLETO.
)
pause
