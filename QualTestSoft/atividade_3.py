"""
Qualidade e Teste de Software
Sistema de Reservas Online para Hotel

Módulos: Login, Pesquisa de Quartos, Reservas e Pagamentos.
"""

from datetime import date, timedelta
from enum import Enum

try:
    from enum import StrEnum
except ImportError:
    class StrEnum(str, Enum):  # type: ignore[no-redef]
        def __str__(self) -> str:
            return self.value


# ── Enums ───────────────────────────────────────────────────────────────────

class TipoQuarto(StrEnum):
    STANDARD = "standard"
    LUXO = "luxo"
    SUITE = "suite"


class MetodoPagamento(StrEnum):
    CARTAO = "cartao"
    PIX = "pix"
    BOLETO = "boleto"


class StatusReserva(StrEnum):
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"
    PAGA = "paga"


# ── Exceções personalizadas ──────────────────────────────────────────────────

class LoginError(Exception):
    pass


class QuartoIndisponivelError(Exception):
    pass


class ReservaError(Exception):
    pass


class PagamentoError(Exception):
    pass


# ── Modelos ──────────────────────────────────────────────────────────────────

class Usuario:
    def __init__(self, email: str, senha: str, nome: str = ""):
        self.email = email
        self.senha = senha
        self.nome = nome


class Quarto:
    def __init__(self, numero: int, tipo: TipoQuarto | str, preco_diaria: float, capacidade: int):
        self.numero = numero
        self.tipo = TipoQuarto(tipo)
        self.preco_diaria = preco_diaria
        self.capacidade = capacidade
        self.disponivel = True

    def __repr__(self):
        return f"Quarto({self.numero}, {self.tipo}, R${self.preco_diaria:.2f})"


class Reserva:
    _contador = 0

    def __init__(self, usuario: Usuario, quarto: Quarto,
                 checkin: date, checkout: date):
        Reserva._contador += 1
        self.id = Reserva._contador
        self.usuario = usuario
        self.quarto = quarto
        self.checkin = checkin
        self.checkout = checkout
        self.status = StatusReserva.CONFIRMADA
        self.pagamento = None

    @property
    def total_diarias(self) -> int:
        return (self.checkout - self.checkin).days

    @property
    def valor_total(self) -> float:
        return self.total_diarias * self.quarto.preco_diaria

    def cancelar(self):
        if self.status == StatusReserva.PAGA:
            raise ReservaError("Não é possível cancelar uma reserva já paga.")
        self.status = StatusReserva.CANCELADA
        self.quarto.disponivel = True

    def __repr__(self):
        return (f"Reserva(id={self.id}, quarto={self.quarto.numero}, "
                f"status={self.status})")


class Pagamento:
    def __init__(self, reserva: Reserva, metodo: MetodoPagamento):
        self.reserva = reserva
        self.metodo = metodo
        self.valor = reserva.valor_total
        self.aprovado = False


# ── Serviços ─────────────────────────────────────────────────────────────────

class SistemaHotel:
    """Classe principal que orquestra o fluxo de reserva do hotel."""

    def __init__(self):
        self.usuarios: list[Usuario] = []
        self.quartos: list[Quarto] = []
        self.reservas: list[Reserva] = []
        self.usuario_logado: Usuario | None = None

    # ── Cadastro / Login ─────────────────────────────────────────────────

    def cadastrar_usuario(self, email: str, senha: str, nome: str = "") -> Usuario:
        if any(u.email == email for u in self.usuarios):
            raise LoginError("E-mail já cadastrado.")
        if len(senha) < 6:
            raise LoginError("A senha deve ter pelo menos 6 caracteres.")
        usuario = Usuario(email, senha, nome)
        self.usuarios.append(usuario)
        return usuario

    def login(self, email: str, senha: str) -> Usuario:
        for u in self.usuarios:
            if u.email == email and u.senha == senha:
                self.usuario_logado = u
                return u
        raise LoginError("E-mail ou senha inválidos.")

    def logout(self):
        self.usuario_logado = None

    # ── Quartos ──────────────────────────────────────────────────────────

    def adicionar_quarto(self, numero: int, tipo: TipoQuarto | str,
                         preco_diaria: float, capacidade: int) -> Quarto:
        if any(q.numero == numero for q in self.quartos):
            raise ValueError("Já existe um quarto com esse número.")
        quarto = Quarto(numero, tipo, preco_diaria, capacidade)
        self.quartos.append(quarto)
        return quarto

    def pesquisar_quartos(self, tipo: TipoQuarto | str | None = None,
                          capacidade_min: int = 1,
                          preco_max: float | None = None,
                          apenas_disponiveis: bool = True) -> list[Quarto]:
        resultado = self.quartos
        if apenas_disponiveis:
            resultado = [q for q in resultado if q.disponivel]
        if tipo:
            resultado = [q for q in resultado if q.tipo == tipo]
        if capacidade_min > 1:
            resultado = [q for q in resultado if q.capacidade >= capacidade_min]
        if preco_max is not None:
            resultado = [q for q in resultado if q.preco_diaria <= preco_max]
        return resultado

    # ── Reservas ─────────────────────────────────────────────────────────

    def criar_reserva(self, numero_quarto: int,
                      checkin: date, checkout: date) -> Reserva:
        if self.usuario_logado is None:
            raise ReservaError("Usuário não está logado.")

        if checkin >= checkout:
            raise ReservaError("A data de check-in deve ser anterior ao check-out.")

        if checkin < date.today():
            raise ReservaError("A data de check-in não pode ser no passado.")

        quarto = self._buscar_quarto(numero_quarto)
        if not quarto.disponivel:
            raise QuartoIndisponivelError(
                f"Quarto {numero_quarto} não está disponível.")

        quarto.disponivel = False
        reserva = Reserva(self.usuario_logado, quarto, checkin, checkout)
        self.reservas.append(reserva)
        return reserva

    def cancelar_reserva(self, reserva_id: int) -> Reserva:
        reserva = self._buscar_reserva(reserva_id)
        reserva.cancelar()
        return reserva

    def listar_reservas_usuario(self) -> list[Reserva]:
        if self.usuario_logado is None:
            raise ReservaError("Usuário não está logado.")
        return [r for r in self.reservas
                if r.usuario.email == self.usuario_logado.email]

    # ── Pagamentos ───────────────────────────────────────────────────────

    def realizar_pagamento(self, reserva_id: int,
                           metodo: MetodoPagamento | str) -> Pagamento:
        try:
            metodo = MetodoPagamento(metodo)
        except ValueError:
            aceitos = ", ".join(m.value for m in MetodoPagamento)
            raise PagamentoError(f"Método inválido. Aceitos: {aceitos}.")

        reserva = self._buscar_reserva(reserva_id)

        if reserva.status == StatusReserva.CANCELADA:
            raise PagamentoError("Não é possível pagar uma reserva cancelada.")
        if reserva.status == StatusReserva.PAGA:
            raise PagamentoError("Reserva já foi paga.")

        pagamento = Pagamento(reserva, metodo)
        pagamento.aprovado = True
        reserva.pagamento = pagamento
        reserva.status = StatusReserva.PAGA
        return pagamento

    # ── Helpers privados ─────────────────────────────────────────────────

    def _buscar_quarto(self, numero: int) -> Quarto:
        for q in self.quartos:
            if q.numero == numero:
                return q
        raise ValueError(f"Quarto {numero} não encontrado.")

    def _buscar_reserva(self, reserva_id: int) -> Reserva:
        for r in self.reservas:
            if r.id == reserva_id:
                return r
        raise ReservaError(f"Reserva {reserva_id} não encontrada.")
