#!/bin/bash

# Script para compilar a função C no Linux/Mac
cd "$(dirname "$0")/.."

echo ""
echo "================================"
echo "  Compilando Função C"
echo "  ConektaAcademy"
echo "================================"
echo ""

# Verificar se gcc está disponível
if ! command -v gcc &> /dev/null; then
    echo "Erro: GCC não encontrado!"
    echo ""
    echo "Instale GCC:"
    echo "  Ubuntu/Debian: sudo apt-get install gcc"
    echo "  Fedora: sudo dnf install gcc"
    echo "  macOS: xcode-select --install"
    echo ""
    exit 1
fi

echo "Compilando calcular_media.c..."

# Determinar o sistema operacional
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    gcc -shared -fPIC -o sistema/calcular_media.dylib sistema/calcular_media.c
    LIB_NAME="calcular_media.dylib"
else
    # Linux
    gcc -shared -fPIC -o sistema/calcular_media.so sistema/calcular_media.c
    LIB_NAME="calcular_media.so"
fi

if [ $? -ne 0 ]; then
    echo ""
    echo "Erro ao compilar!"
    echo "Verifique se o arquivo calcular_media.c existe na pasta sistema/"
    exit 1
fi

echo ""
echo "================================"
echo "  Compilação concluída!"
echo "================================"
echo ""
echo "Arquivo gerado: sistema/$LIB_NAME"
echo ""
echo "O sistema agora usará a função C para calcular médias."
echo ""

