# Fluxo de Testes — Sistema de Reservas Online para Hotel

## Visão Geral

O sistema (`atividade_3.py`) implementa um **Sistema de Reservas Online para Hotel** com quatro módulos principais: **Login**, **Quartos**, **Reservas** e **Pagamentos**. Os testes (`test_atividade_3.py`) validam cada módulo isoladamente e, ao final, simulam o fluxo completo de ponta a ponta.

**Framework utilizado:** `unittest` (biblioteca padrão do Python)  
**Execução:** `python -m pytest test_atividade_3.py -v`

---

## Estrutura do Sistema Sob Teste

### Enums

| Enum | Valores | Descrição |
|------|---------|-----------|
| `TipoQuarto` | `STANDARD`, `LUXO`, `SUITE` | Categorias de quarto disponíveis |
| `MetodoPagamento` | `CARTAO`, `PIX`, `BOLETO` | Formas de pagamento aceitas |
| `StatusReserva` | `CONFIRMADA`, `CANCELADA`, `PAGA` | Ciclo de vida de uma reserva |

### Exceções Personalizadas

| Exceção | Quando é lançada |
|---------|-----------------|
| `LoginError` | Cadastro/login inválidos (e-mail duplicado, senha curta, credenciais erradas) |
| `QuartoIndisponivelError` | Tentativa de reservar quarto já ocupado |
| `ReservaError` | Operações de reserva inválidas (sem login, datas incoerentes, cancelar reserva paga, etc.) |
| `PagamentoError` | Pagamento inválido (método incorreto, reserva cancelada ou já paga) |

### Modelos de Dados

- **`Usuario`** — e-mail, senha e nome.
- **`Quarto`** — número, tipo, preço da diária, capacidade e flag `disponivel`.
- **`Reserva`** — referência ao usuário e quarto, datas de check-in/check-out, status e pagamento. Possui propriedades calculadas `total_diarias` e `valor_total`.
- **`Pagamento`** — referência à reserva, método, valor e flag `aprovado`.

### Classe Principal: `SistemaHotel`

Orquestra todo o fluxo e mantém as listas de usuários, quartos e reservas, além do `usuario_logado`.

---

## Organização dos Testes

Os testes estão divididos em **5 classes** que seguem a ordem lógica do fluxo de uso:

```
TestCadastroLogin  →  TestQuartos  →  TestReservas  →  TestPagamento  →  TestFluxoCompleto
```

### Função Helper

```python
_hotel_com_quartos() -> SistemaHotel
```

Cria e retorna um `SistemaHotel` já configurado com 4 quartos (101 Standard, 102 Standard, 201 Luxo, 301 Suíte) e um usuário logado (`joao@email.com`). Utilizada nos `setUp` de `TestReservas` e `TestPagamento` para evitar duplicação.

---

## 1. `TestCadastroLogin` — Cadastro e Autenticação

Valida todo o ciclo de autenticação do usuário.

| # | Teste | O que verifica | Resultado esperado |
|---|-------|---------------|--------------------|
| 1 | `test_cadastrar_usuario_com_sucesso` | Cadastro com dados válidos | Usuário criado, lista tem 1 item |
| 2 | `test_cadastrar_email_duplicado` | Cadastro com e-mail já existente | Lança `LoginError` |
| 3 | `test_cadastrar_senha_curta` | Senha com menos de 6 caracteres | Lança `LoginError` |
| 4 | `test_login_com_sucesso` | Login com credenciais corretas | Retorna o usuário, atualiza `usuario_logado` |
| 5 | `test_login_credenciais_invalidas` | Login com senha errada | Lança `LoginError` |
| 6 | `test_logout` | Encerramento de sessão | `usuario_logado` volta a ser `None` |

**Fluxo coberto:**

```
cadastrar_usuario() → login() → logout()
```

---

## 2. `TestQuartos` — Pesquisa de Quartos

Valida o cadastro e a pesquisa de quartos com diferentes filtros.

| # | Teste | O que verifica | Resultado esperado |
|---|-------|---------------|--------------------|
| 1 | `test_adicionar_quarto_numero_duplicado` | Quarto com número já cadastrado | Lança `ValueError` |
| 2 | `test_pesquisar_todos_disponiveis` | Pesquisa sem filtros | Retorna 3 quartos |
| 3 | `test_pesquisar_por_tipo` | Filtro por tipo (`LUXO`) | Retorna apenas quarto 201 |
| 4 | `test_pesquisar_por_capacidade_minima` | Filtro por capacidade ≥ 3 | Retorna 2 quartos (Luxo e Suíte) |
| 5 | `test_pesquisar_por_preco_maximo` | Filtro por diária ≤ R$450 | Retorna 2 quartos (Standard e Luxo) |
| 6 | `test_pesquisar_quarto_indisponivel_oculto` | Quarto indisponível é omitido | Retorna 2 quartos |
| 7 | `test_pesquisar_incluindo_indisponiveis` | Flag `apenas_disponiveis=False` | Retorna todos os 3 quartos |

**Fluxo coberto:**

```
adicionar_quarto() → pesquisar_quartos(filtros)
```

---

## 3. `TestReservas` — Criação e Cancelamento de Reservas

Valida as regras de negócio para criar e cancelar reservas.

| # | Teste | O que verifica | Resultado esperado |
|---|-------|---------------|--------------------|
| 1 | `test_criar_reserva_com_sucesso` | Reserva com dados válidos | Status `CONFIRMADA`, 3 diárias, valor R$600 |
| 2 | `test_criar_reserva_quarto_fica_indisponivel` | Quarto marcado como indisponível após reserva | `quarto.disponivel == False` |
| 3 | `test_criar_reserva_sem_login` | Reserva sem usuário logado | Lança `ReservaError` |
| 4 | `test_criar_reserva_checkin_depois_checkout` | Check-in posterior ao check-out | Lança `ReservaError` |
| 5 | `test_criar_reserva_checkin_igual_checkout` | Datas iguais de check-in e check-out | Lança `ReservaError` |
| 6 | `test_criar_reserva_checkin_no_passado` | Check-in com data no passado | Lança `ReservaError` |
| 7 | `test_criar_reserva_quarto_indisponivel` | Reserva de quarto já reservado | Lança `QuartoIndisponivelError` |
| 8 | `test_criar_reserva_quarto_inexistente` | Quarto com número que não existe | Lança `ValueError` |
| 9 | `test_cancelar_reserva` | Cancelamento de reserva confirmada | Status muda para `CANCELADA` |
| 10 | `test_cancelar_reserva_libera_quarto` | Quarto volta a ficar disponível após cancelamento | `quarto.disponivel == True` |
| 11 | `test_cancelar_reserva_paga_falha` | Cancelamento de reserva já paga | Lança `ReservaError` |
| 12 | `test_cancelar_reserva_inexistente` | Cancelamento com ID inexistente | Lança `ReservaError` |
| 13 | `test_listar_reservas_do_usuario` | Listagem das reservas do usuário logado | Retorna 2 reservas |
| 14 | `test_listar_reservas_sem_login` | Listagem sem estar logado | Lança `ReservaError` |

**Fluxo coberto:**

```
criar_reserva() → cancelar_reserva() → listar_reservas_usuario()
```

---

## 4. `TestPagamento` — Processamento de Pagamentos

Valida pagamentos com diferentes métodos e caminhos de erro.

| # | Teste | O que verifica | Resultado esperado |
|---|-------|---------------|--------------------|
| 1 | `test_pagamento_cartao_com_sucesso` | Pagamento via cartão | `aprovado=True`, método `CARTAO`, valor R$600 |
| 2 | `test_pagamento_pix_com_sucesso` | Pagamento via PIX | `aprovado=True` |
| 3 | `test_pagamento_boleto_com_sucesso` | Pagamento via boleto | `aprovado=True` |
| 4 | `test_pagamento_atualiza_status_reserva` | Status da reserva após pagamento | Status muda para `PAGA` |
| 5 | `test_pagamento_metodo_invalido` | Método de pagamento inexistente (`"crypto"`) | Lança `PagamentoError` |
| 6 | `test_pagamento_reserva_cancelada` | Pagamento de reserva já cancelada | Lança `PagamentoError` |
| 7 | `test_pagamento_duplicado` | Segundo pagamento na mesma reserva | Lança `PagamentoError` |
| 8 | `test_pagamento_reserva_inexistente` | Pagamento com ID de reserva inválido | Lança `ReservaError` |

**Fluxo coberto:**

```
realizar_pagamento(metodo) → validações de estado da reserva
```

---

## 5. `TestFluxoCompleto` — Teste de Integração (Ponta a Ponta)

Simula cenários reais do início ao fim, sem o `setUp` da helper.

### 5.1 `test_fluxo_reserva_completo`

```
Adicionar quartos → Cadastrar usuário → Login → Pesquisar quartos (tipo Luxo)
→ Criar reserva (3 noites, R$1350) → Verificar quarto sumiu da pesquisa → Pagar com cartão
```

**Validações:**
- Pesquisa retorna 1 quarto luxo antes da reserva e 0 depois.
- Reserva fica com status `CONFIRMADA` e valor `R$1.350,00` (3 × R$450).
- Pagamento aprovado, status final `PAGA`.

### 5.2 `test_fluxo_reserva_e_cancelamento`

```
Adicionar quarto → Cadastrar usuário → Login → Criar reserva → Cancelar reserva
→ Verificar quarto disponível novamente
```

**Validações:**
- Reserva cancelada com status `CANCELADA`.
- Quarto volta a aparecer na pesquisa como disponível.

---

## Diagrama do Ciclo de Vida da Reserva

```
                    ┌─────────────┐
                    │  CONFIRMADA │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │                         │
              ▼                         ▼
     ┌────────────────┐       ┌─────────────────┐
     │   CANCELADA    │       │      PAGA       │
     │ (quarto livre) │       │ (não cancelável) │
     └────────────────┘       └─────────────────┘
```

---

## Cobertura por Tipo de Teste

| Tipo | Quantidade | Descrição |
|------|:----------:|-----------|
| Caminho feliz (sucesso) | 18 | Fluxos onde tudo funciona corretamente |
| Caminho de erro (exceções) | 17 | Validações de input, estado e permissão |
| Integração (ponta a ponta) | 2 | Fluxos completos simulando uso real |
| **Total** | **37** | — |

---

## Como Executar

```bash
# Na raiz do projeto QualTestSoft/
python -m pytest test_atividade_3.py -v
```

Saída esperada: **37 testes passando**.
