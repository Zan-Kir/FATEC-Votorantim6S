"""
Testes unitários – Sistema de Reservas Online para Hotel
Execução: python -m pytest test_atividade_3.py -v
"""

import unittest
from datetime import date, timedelta

from atividade_3 import (
    SistemaHotel,
    LoginError,
    QuartoIndisponivelError,
    ReservaError,
    PagamentoError,
    TipoQuarto,
    MetodoPagamento,
    StatusReserva,
)


def _hotel_com_quartos() -> SistemaHotel:
    """Helper: retorna um sistema já populado com quartos e um usuário logado."""
    h = SistemaHotel()
    h.adicionar_quarto(101, TipoQuarto.STANDARD, 200.0, 2)
    h.adicionar_quarto(102, TipoQuarto.STANDARD, 220.0, 2)
    h.adicionar_quarto(201, TipoQuarto.LUXO, 450.0, 3)
    h.adicionar_quarto(301, TipoQuarto.SUITE, 800.0, 4)
    h.cadastrar_usuario("joao@email.com", "senha123", "João")
    h.login("joao@email.com", "senha123")
    return h


# ═══════════════════════════════════════════════════════════════════════════════
#  1. Testes de Cadastro / Login
# ═══════════════════════════════════════════════════════════════════════════════

class TestCadastroLogin(unittest.TestCase):

    def setUp(self):
        self.hotel = SistemaHotel()

    def test_cadastrar_usuario_com_sucesso(self):
        u = self.hotel.cadastrar_usuario("ana@email.com", "abc123", "Ana")
        self.assertEqual(u.email, "ana@email.com")
        self.assertEqual(len(self.hotel.usuarios), 1)

    def test_cadastrar_email_duplicado(self):
        self.hotel.cadastrar_usuario("ana@email.com", "abc123")
        with self.assertRaises(LoginError):
            self.hotel.cadastrar_usuario("ana@email.com", "outra1")

    def test_cadastrar_senha_curta(self):
        with self.assertRaises(LoginError):
            self.hotel.cadastrar_usuario("ana@email.com", "123")

    def test_login_com_sucesso(self):
        self.hotel.cadastrar_usuario("ana@email.com", "abc123", "Ana")
        u = self.hotel.login("ana@email.com", "abc123")
        self.assertEqual(u.nome, "Ana")
        self.assertIs(self.hotel.usuario_logado, u)

    def test_login_credenciais_invalidas(self):
        self.hotel.cadastrar_usuario("ana@email.com", "abc123")
        with self.assertRaises(LoginError):
            self.hotel.login("ana@email.com", "errada")

    def test_logout(self):
        self.hotel.cadastrar_usuario("ana@email.com", "abc123")
        self.hotel.login("ana@email.com", "abc123")
        self.hotel.logout()
        self.assertIsNone(self.hotel.usuario_logado)


# ═══════════════════════════════════════════════════════════════════════════════
#  2. Testes de Quartos
# ═══════════════════════════════════════════════════════════════════════════════

class TestQuartos(unittest.TestCase):

    def setUp(self):
        self.hotel = SistemaHotel()
        self.hotel.adicionar_quarto(101, TipoQuarto.STANDARD, 200.0, 2)
        self.hotel.adicionar_quarto(201, TipoQuarto.LUXO, 450.0, 3)
        self.hotel.adicionar_quarto(301, TipoQuarto.SUITE, 800.0, 4)

    def test_adicionar_quarto_numero_duplicado(self):
        with self.assertRaises(ValueError):
            self.hotel.adicionar_quarto(101, "standard", 210.0, 2)

    def test_pesquisar_todos_disponiveis(self):
        resultado = self.hotel.pesquisar_quartos()
        self.assertEqual(len(resultado), 3)

    def test_pesquisar_por_tipo(self):
        resultado = self.hotel.pesquisar_quartos(tipo=TipoQuarto.LUXO)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].numero, 201)

    def test_pesquisar_por_capacidade_minima(self):
        resultado = self.hotel.pesquisar_quartos(capacidade_min=3)
        self.assertEqual(len(resultado), 2)  # luxo(3) e suite(4)

    def test_pesquisar_por_preco_maximo(self):
        resultado = self.hotel.pesquisar_quartos(preco_max=450.0)
        self.assertEqual(len(resultado), 2)  # standard(200) e luxo(450)

    def test_pesquisar_quarto_indisponivel_oculto(self):
        self.hotel.quartos[0].disponivel = False
        resultado = self.hotel.pesquisar_quartos()
        self.assertEqual(len(resultado), 2)

    def test_pesquisar_incluindo_indisponiveis(self):
        self.hotel.quartos[0].disponivel = False
        resultado = self.hotel.pesquisar_quartos(apenas_disponiveis=False)
        self.assertEqual(len(resultado), 3)


# ═══════════════════════════════════════════════════════════════════════════════
#  3. Testes de Reservas
# ═══════════════════════════════════════════════════════════════════════════════

class TestReservas(unittest.TestCase):

    def setUp(self):
        self.hotel = _hotel_com_quartos()
        self.checkin = date.today() + timedelta(days=5)
        self.checkout = date.today() + timedelta(days=8)

    def test_criar_reserva_com_sucesso(self):
        reserva = self.hotel.criar_reserva(101, self.checkin, self.checkout)
        self.assertEqual(reserva.status, StatusReserva.CONFIRMADA)
        self.assertEqual(reserva.total_diarias, 3)
        self.assertAlmostEqual(reserva.valor_total, 600.0)

    def test_criar_reserva_quarto_fica_indisponivel(self):
        self.hotel.criar_reserva(101, self.checkin, self.checkout)
        quarto = self.hotel._buscar_quarto(101)
        self.assertFalse(quarto.disponivel)

    def test_criar_reserva_sem_login(self):
        self.hotel.logout()
        with self.assertRaises(ReservaError):
            self.hotel.criar_reserva(101, self.checkin, self.checkout)

    def test_criar_reserva_checkin_depois_checkout(self):
        with self.assertRaises(ReservaError):
            self.hotel.criar_reserva(101, self.checkout, self.checkin)

    def test_criar_reserva_checkin_igual_checkout(self):
        with self.assertRaises(ReservaError):
            self.hotel.criar_reserva(101, self.checkin, self.checkin)

    def test_criar_reserva_checkin_no_passado(self):
        passado = date.today() - timedelta(days=1)
        with self.assertRaises(ReservaError):
            self.hotel.criar_reserva(101, passado, self.checkout)

    def test_criar_reserva_quarto_indisponivel(self):
        self.hotel.criar_reserva(101, self.checkin, self.checkout)
        with self.assertRaises(QuartoIndisponivelError):
            self.hotel.criar_reserva(101, self.checkin, self.checkout)

    def test_criar_reserva_quarto_inexistente(self):
        with self.assertRaises(ValueError):
            self.hotel.criar_reserva(999, self.checkin, self.checkout)

    def test_cancelar_reserva(self):
        reserva = self.hotel.criar_reserva(101, self.checkin, self.checkout)
        self.hotel.cancelar_reserva(reserva.id)
        self.assertEqual(reserva.status, StatusReserva.CANCELADA)

    def test_cancelar_reserva_libera_quarto(self):
        reserva = self.hotel.criar_reserva(101, self.checkin, self.checkout)
        self.hotel.cancelar_reserva(reserva.id)
        quarto = self.hotel._buscar_quarto(101)
        self.assertTrue(quarto.disponivel)

    def test_cancelar_reserva_paga_falha(self):
        reserva = self.hotel.criar_reserva(101, self.checkin, self.checkout)
        self.hotel.realizar_pagamento(reserva.id, MetodoPagamento.PIX)
        with self.assertRaises(ReservaError):
            self.hotel.cancelar_reserva(reserva.id)

    def test_cancelar_reserva_inexistente(self):
        with self.assertRaises(ReservaError):
            self.hotel.cancelar_reserva(9999)

    def test_listar_reservas_do_usuario(self):
        self.hotel.criar_reserva(101, self.checkin, self.checkout)
        self.hotel.criar_reserva(201, self.checkin, self.checkout)
        reservas = self.hotel.listar_reservas_usuario()
        self.assertEqual(len(reservas), 2)

    def test_listar_reservas_sem_login(self):
        self.hotel.logout()
        with self.assertRaises(ReservaError):
            self.hotel.listar_reservas_usuario()


# ═══════════════════════════════════════════════════════════════════════════════
#  4. Testes de Pagamento
# ═══════════════════════════════════════════════════════════════════════════════

class TestPagamento(unittest.TestCase):

    def setUp(self):
        self.hotel = _hotel_com_quartos()
        checkin = date.today() + timedelta(days=5)
        checkout = date.today() + timedelta(days=8)
        self.reserva = self.hotel.criar_reserva(101, checkin, checkout)

    def test_pagamento_cartao_com_sucesso(self):
        pag = self.hotel.realizar_pagamento(self.reserva.id, MetodoPagamento.CARTAO)
        self.assertTrue(pag.aprovado)
        self.assertEqual(pag.metodo, MetodoPagamento.CARTAO)
        self.assertAlmostEqual(pag.valor, 600.0)

    def test_pagamento_pix_com_sucesso(self):
        pag = self.hotel.realizar_pagamento(self.reserva.id, MetodoPagamento.PIX)
        self.assertTrue(pag.aprovado)

    def test_pagamento_boleto_com_sucesso(self):
        pag = self.hotel.realizar_pagamento(self.reserva.id, MetodoPagamento.BOLETO)
        self.assertTrue(pag.aprovado)

    def test_pagamento_atualiza_status_reserva(self):
        self.hotel.realizar_pagamento(self.reserva.id, MetodoPagamento.PIX)
        self.assertEqual(self.reserva.status, StatusReserva.PAGA)

    def test_pagamento_metodo_invalido(self):
        with self.assertRaises(PagamentoError):
            self.hotel.realizar_pagamento(self.reserva.id, "crypto")

    def test_pagamento_reserva_cancelada(self):
        self.hotel.cancelar_reserva(self.reserva.id)
        with self.assertRaises(PagamentoError):
            self.hotel.realizar_pagamento(self.reserva.id, MetodoPagamento.PIX)

    def test_pagamento_duplicado(self):
        self.hotel.realizar_pagamento(self.reserva.id, MetodoPagamento.PIX)
        with self.assertRaises(PagamentoError):
            self.hotel.realizar_pagamento(self.reserva.id, MetodoPagamento.CARTAO)

    def test_pagamento_reserva_inexistente(self):
        with self.assertRaises(ReservaError):
            self.hotel.realizar_pagamento(9999, MetodoPagamento.PIX)


# ═══════════════════════════════════════════════════════════════════════════════
#  5. Teste de Fluxo Completo (Sistema)
# ═══════════════════════════════════════════════════════════════════════════════

class TestFluxoCompleto(unittest.TestCase):
    """Simula o fluxo completo: cadastro → login → pesquisa → reserva → pagamento."""

    def test_fluxo_reserva_completo(self):
        hotel = SistemaHotel()

        # Adicionar quartos
        hotel.adicionar_quarto(101, TipoQuarto.STANDARD, 200.0, 2)
        hotel.adicionar_quarto(201, TipoQuarto.LUXO, 450.0, 3)

        # Cadastro e login
        hotel.cadastrar_usuario("maria@email.com", "segura123", "Maria")
        hotel.login("maria@email.com", "segura123")

        # Pesquisar quartos disponíveis do tipo luxo
        disponiveis = hotel.pesquisar_quartos(tipo=TipoQuarto.LUXO)
        self.assertEqual(len(disponiveis), 1)

        # Criar reserva
        checkin = date.today() + timedelta(days=10)
        checkout = date.today() + timedelta(days=13)
        reserva = hotel.criar_reserva(201, checkin, checkout)
        self.assertEqual(reserva.status, StatusReserva.CONFIRMADA)
        self.assertAlmostEqual(reserva.valor_total, 1350.0)  # 3 × 450

        # Quarto deve sumir da pesquisa
        disponiveis = hotel.pesquisar_quartos(tipo=TipoQuarto.LUXO)
        self.assertEqual(len(disponiveis), 0)

        # Pagamento
        pagamento = hotel.realizar_pagamento(reserva.id, MetodoPagamento.CARTAO)
        self.assertTrue(pagamento.aprovado)
        self.assertEqual(reserva.status, StatusReserva.PAGA)

    def test_fluxo_reserva_e_cancelamento(self):
        hotel = SistemaHotel()
        hotel.adicionar_quarto(101, TipoQuarto.STANDARD, 200.0, 2)
        hotel.cadastrar_usuario("pedro@email.com", "minhasenha", "Pedro")
        hotel.login("pedro@email.com", "minhasenha")

        checkin = date.today() + timedelta(days=3)
        checkout = date.today() + timedelta(days=5)
        reserva = hotel.criar_reserva(101, checkin, checkout)

        # Cancelar antes de pagar
        hotel.cancelar_reserva(reserva.id)
        self.assertEqual(reserva.status, StatusReserva.CANCELADA)

        # Quarto fica disponível novamente
        disponiveis = hotel.pesquisar_quartos(tipo=TipoQuarto.STANDARD)
        self.assertEqual(len(disponiveis), 1)


if __name__ == "__main__":
    unittest.main()
