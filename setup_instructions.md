# Configuração do Ambiente para QGSS 2025 Team07

Este documento contém instruções para configurar um ambiente Anaconda com todas as bibliotecas necessárias para executar os laboratórios do QGSS 2025 (labs 0-4, community-labs e functions-labs).

## Pré-requisitos
- Anaconda ou Miniconda instalado no seu sistema

## Passo 1: Criar o ambiente a partir do arquivo environment.yml

```bash
# Navegue até o diretório do projeto
cd /home/test/Downloads/IBM/qgss25/qgss-2025-team07/

# Crie o ambiente usando o arquivo environment.yml
conda env create -f environment.yml
```

## Passo 2: Ativar o ambiente

```bash
conda activate qgss-2025
```

## Passo 3: Verificar a instalação

```bash
# Verificar versão do Qiskit
python -c "import qiskit; print(qiskit.__version__)"

# Verificar versão do Qiskit IBM Runtime
python -c "import qiskit_ibm_runtime; print(qiskit_ibm_runtime.__version__)"

# Verificar versão do Qiskit Aer
python -c "import qiskit_aer; print(qiskit_aer.__version__)"
```

## Passo 4: Iniciar o JupyterLab para trabalhar com os notebooks

```bash
jupyter lab
```

## Problemas conhecidos e soluções

Se você encontrar problemas com alguma biblioteca específica, tente instalar manualmente:

```bash
pip install nome-da-biblioteca==versão
```

Para problemas com o qc-grader, você pode reinstalar diretamente:

```bash
pip install "qc-grader[jupyter,qiskit] @ git+https://github.com/qiskit-community/Quantum-Challenge-Grader.git"
```

## Observações

Este ambiente foi configurado com base na análise das dependências do repositório `qgss-2025-team07`. Se houver discrepâncias com o repositório oficial `qgss-2025-oficial`, pode ser necessário ajustar as versões ou adicionar/remover pacotes.

## Bibliotecas incluídas

### Pacotes principais do Qiskit:
- qiskit (2.1.1)
- qiskit-ibm-runtime (0.40.0)
- qiskit-aer (0.17.1)
- qiskit-ibm-catalog (0.8.0)
- qiskit_serverless (0.25.1)

### Bibliotecas científicas:
- numpy (2.3.1)
- scipy (1.16.0)
- matplotlib (3.10.3)
- pandas
- sympy (1.14.0)
- pyscf (2.9.0)
- networkx (3.5)

### Utilitários:
- dill (0.4.0)
- tqdm (4.67.1)
- pylatexenc
- pydot (4.0.1)
- seaborn (0.13.2)
- pillow (11.3.0)
- pyarrow (18.1.0)

### Bibliotecas para desenvolvimento:
- jupyter (1.1.1)
- jupyterlab (4.4.4)
- ipywidgets

### Bibliotecas para autenticação e comunicação:
- requests (2.32.3)
- requests-ntlm (1.3.0)
- urllib3 (2.5.0)
- ibm-platform-services (0.66.1)
- ibm_cloud_sdk_core (3.24.1)
- python-dateutil (2.9.0.post0)
- cryptography (45.0.5)
