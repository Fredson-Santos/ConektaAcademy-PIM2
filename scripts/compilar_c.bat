@echo off
REM Script para compilar a função C no Windows
cd /d "%~dp0\.."

echo.
echo ================================
echo  Compilando Função C
echo  ConektaAcademy
echo ================================
echo.

REM Verificar se gcc está disponível
gcc --version >nul 2>&1
if errorlevel 1 (
    echo Erro: GCC nao encontrado!
    echo.
    echo Instale MinGW-w64 de: https://www.mingw-w64.org/
    echo Ou use Visual Studio com MSVC
    echo.
    pause
    exit /b 1
)

echo Compilando calcular_media.c...
gcc -shared -o sistema\calcular_media.dll sistema\calcular_media.c

if errorlevel 1 (
    echo.
    echo Erro ao compilar!
    echo Verifique se o arquivo calcular_media.c existe na pasta sistema\
    pause
    exit /b 1
)

echo.
echo ================================
echo  Compilacao concluida!
echo ================================
echo.
echo Arquivo gerado: sistema\calcular_media.dll
echo.
echo O sistema agora usara a funcao C para calcular medias.
echo.
pause

