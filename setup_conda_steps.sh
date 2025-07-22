#!/bin/bash

# Script para instalar ambiente QGSS 2025 em etapas para resolver conflitos de dependências

echo "Iniciando instalação do ambiente QGSS 2025 em etapas..."

# Criar o ambiente base com Python e dependências básicas
echo "Etapa 1: Criando ambiente base com Python 3.11..."
conda create -n qgss-2025-step python=3.11 pip numpy=2.3.1 scipy=1.16.0 matplotlib=3.10.3 pandas sympy=1.14.0 networkx=3.2.1 jupyterlab jupyter ipywidgets -y

# Ativar o ambiente
echo "Ativando ambiente conda..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate qgss-2025-step

# Instalar qiskit e dependências principais
echo "Etapa 2: Instalando Qiskit e dependências principais..."
pip install "qiskit==2.1.1" "qiskit-ibm-runtime==0.40.0" "qiskit-aer==0.17.1"

# Instalar o grader que vai puxar dependências compatíveis
echo "Etapa 3: Instalando QC Grader..."
pip install "qc-grader[jupyter,qiskit] @ git+https://github.com/qiskit-community/Quantum-Challenge-Grader.git"

# Instalar o qiskit-ibm-catalog com versão compatível
echo "Etapa 4: Instalando Qiskit IBM Catalog..."
pip install "qiskit-ibm-catalog>=0.8.0"

# Instalar outras dependências
echo "Etapa 5: Instalando demais dependências..."
pip install pylatexenc pydot==4.0.1 pyscf==2.9.0 stevedore==5.4.1 rustworkx==0.16.0 symengine==0.13.0

echo "Instalação em etapas concluída!"
echo "Para ativar o ambiente, execute: conda activate qgss-2025-step"
echo "Para verificar a instalação, execute: python -c \"import qiskit; print(qiskit.__version__)\""
