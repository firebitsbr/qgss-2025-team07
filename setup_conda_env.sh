#!/bin/bash

# Script para configurar ambiente Anaconda para QGSS 2025 Team07

echo "Iniciando configuração do ambiente para QGSS 2025 Team07..."

# Verificar se o conda está instalado
if ! command -v conda &> /dev/null; then
    echo "Erro: Anaconda/Miniconda não está instalado ou não está no PATH."
    echo "Por favor, instale Anaconda/Miniconda e tente novamente."
    exit 1
fi

# Criar o ambiente a partir do arquivo environment.yml
echo "Criando ambiente conda a partir de environment.yml..."
conda env create -f environment.yml

if [ $? -ne 0 ]; then
    echo "Erro ao criar o ambiente conda. Verifique o arquivo environment.yml."
    exit 1
fi

echo "Ambiente 'qgss-2025' criado com sucesso!"

echo "Para ativar o ambiente, execute: conda activate qgss-2025"
echo "Para iniciar JupyterLab, execute: jupyter lab"

# Instruções para verificação
echo ""
echo "Para verificar a instalação, ative o ambiente e execute:"
echo "python -c \"import qiskit; print(qiskit.__version__)\""
echo "python -c \"import qiskit_ibm_runtime; print(qiskit_ibm_runtime.__version__)\""
echo "python -c \"import qiskit_aer; print(qiskit_aer.__version__)\""

exit 0
