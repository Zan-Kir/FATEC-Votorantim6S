# Ambiente Python — ProcLingNatural

Instruções rápidas para criar e ativar um ambiente Python nesta pasta.

1) Criar o ambiente (se ainda não foi criado):

- PowerShell / CMD (Windows):

```
python -m venv .venv
```

2) Ativar o ambiente:

- PowerShell:

```
.\.venv\Scripts\Activate.ps1
```

- CMD:

```
.\.venv\Scripts\activate.bat
```

- Git Bash / WSL / macOS / Linux:

```
source .venv/bin/activate
```

3) Verificar o Python ativo:

```
python --version
pip --version
```

4) Instalar dependências (exemplo):

```
pip install -r requirements.txt
```

Observação: a ferramenta de configuração já preparou um ambiente virtual em `.venv` na raiz do workspace. Se preferir outro nome de pasta, substitua `.venv` acima.

## Script de ativação automática

Criei um script PowerShell para facilitar a ativação do ambiente:

- Arquivo: `run_env.ps1`

Uso:

- Para abrir uma nova janela PowerShell com o ambiente ativado (execução padrão):

```powershell
.\run_env.ps1
```

- Para ativar o ambiente na sessão PowerShell atual (dot-source):

```powershell
#. .\run_env.ps1
```

O script tentará localizar `.venv\Scripts\Activate.ps1` e exibirá uma mensagem de erro se não encontrar o virtualenv.
