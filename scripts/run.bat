@echo off
REM Script para executar o Sistema Acadêmico com Streamlit
cd /d "%~dp0\.."

echo.
echo ================================
echo  ConektaAcademy - Streamlit
echo ================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo Erro: Python nao encontrado!
    echo Instale Python de: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Verificar se streamlit está instalado
python -m pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Erro ao instalar dependencias!
        pause
        exit /b 1
    )
)

echo Iniciando ConektaAcademy...
echo.
echo A aplicacao sera aberta em: http://localhost:8501
echo Pressione Ctrl+C para encerrar
echo.

python -m streamlit run interface/app.py

pause
