# run_env.ps1
# Abre uma nova janela PowerShell com o ambiente virtual `.venv` ativado.
# Uso: execute este script normalmente (duplo-clique) para abrir nova janela,
# ou dot-source (`. .\run_env.ps1`) para ativar no shell atual.

$venv = Join-Path $PSScriptRoot '.venv\Scripts\Activate.ps1'

if (-not (Test-Path $venv)) {
    Write-Error "Virtualenv não encontrado em '.venv'. Crie com: python -m venv .venv"
    exit 1
}

# Se o script for dot-sourced, apenas execute o activation no mesmo processo.
if ($MyInvocation.InvocationName -eq '.') {
    & $venv
    return
}

# Caso contrário, abre uma nova janela PowerShell com o venv ativado e mantém a janela aberta.
$arg = "-NoExit -ExecutionPolicy Bypass -Command \"& '$venv'\""
Start-Process powershell -ArgumentList $arg
Write-Host "Abrindo nova janela PowerShell com o ambiente ativado..."
