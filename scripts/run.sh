#!/bin/bash

# Script para executar o Sistema Acadêmico com Streamlit
cd "$(dirname "$0")/.."

echo ""
echo "================================"
echo "  ConektaAcademy - Streamlit"
echo "================================"
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Erro: Python3 não encontrado!"
    echo "Instale Python de: https://www.python.org/downloads/"
    exit 1
fi

# Verificar se streamlit está instalado
if ! python3 -m pip show streamlit &> /dev/null; then
    echo "Instalando dependências..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Erro ao instalar dependências!"
        exit 1
    fi
fi

echo "Iniciando ConektaAcademy..."
echo ""
echo "A aplicação será aberta em: http://localhost:8501"
echo "Pressione Ctrl+C para encerrar"
echo ""

python3 -m streamlit run interface/app.py
