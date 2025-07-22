# Configuração do Ambiente para QGSS 2025

Este repositório contém instruções e scripts para configurar um ambiente Anaconda compatível com o QGSS 2025.

## Opções de Instalação

Devido a possíveis conflitos de dependências, fornecemos três opções diferentes para configurar seu ambiente:

### Opção 1: Instalação com environment.yml atualizado

```bash
# Criar o ambiente a partir do arquivo environment.yml atualizado
conda env create -f environment.yml
```

### Opção 2: Instalação com environment-alt.yml (versões mais flexíveis)

```bash
# Criar o ambiente a partir de um arquivo alternativo
conda env create -f environment-alt.yml
```

### Opção 3: Instalação em etapas (recomendado em caso de conflitos)

```bash
# Executar a instalação em etapas para evitar conflitos
./setup_conda_steps.sh
```

## Uso no Visual Studio Code

1. Instale a extensão Python no VS Code
2. Selecione o interpretador Python no canto inferior esquerdo do VS Code
3. Escolha o ambiente conda que você criou (qgss-2025 ou qgss-2025-alt ou qgss-2025-step)
4. Ao abrir notebooks, selecione este kernel nas opções

## Verificação da Instalação

Para verificar se o ambiente está configurado corretamente, execute:

```python
import qiskit
import qiskit_ibm_runtime
import qiskit_aer
import numpy
import matplotlib

print(f"Qiskit: {qiskit.__version__}")
print(f"Qiskit IBM Runtime: {qiskit_ibm_runtime.__version__}")
print(f"Qiskit Aer: {qiskit_aer.__version__}")
print(f"NumPy: {numpy.__version__}")
print(f"Matplotlib: {matplotlib.__version__}")
```

## Resolução de Problemas

Se você encontrar conflitos de dependências, tente:

1. Usar o método de instalação em etapas (Opção 3)
2. Instalar manualmente pacotes específicos após a criação do ambiente
3. Ajustar as versões no arquivo environment.yml

## Notas Importantes

- O erro principal encontrado está relacionado a conflitos entre `qiskit_serverless`, `qiskit-ibm-catalog` e `qc-grader`.
- A ordem de instalação dos pacotes pode afetar a resolução de dependências.
- Em alguns casos, pode ser necessário instalar versões específicas para resolver conflitos.
