import unittest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.estoque import (
    Produto,
    Estoque,
    ProdutoInvalidoError,
    EstoqueInsuficienteError,
    ProdutoNaoEncontradoError,
    CategoriaInvalidaError,
)


class TestProduto(unittest.TestCase):

    def test_criar_produto_valido(self):
        # Deve criar produto com todos os atributos corretos
        p = Produto("P001", "Caneta Azul", 2.50, 100)
        self.assertEqual(p.codigo, "P001")
        self.assertEqual(p.nome, "Caneta Azul")
        self.assertAlmostEqual(p.preco, 2.50)
        self.assertEqual(p.quantidade, 100)

    def test_codigo_normalizado_para_maiusculas(self):
        # O código deve ser armazenado em maiúsculas
        p = Produto("abc", "Produto X", 10.0)
        self.assertEqual(p.codigo, "ABC")

    def test_produto_sem_quantidade_inicial(self):
        # Produto criado sem quantidade deve ter quantidade 0
        p = Produto("P002", "Lápis", 1.00)
        self.assertEqual(p.quantidade, 0)

    def test_valor_total_produto(self):
        # Deve calcular corretamente o valor total em estoque
        p = Produto("P003", "Borracha", 1.50, 40)
        self.assertAlmostEqual(p.valor_total(), 60.0)

    def test_valor_total_produto_sem_estoque(self):
        # Valor total de produto sem estoque deve ser 0
        p = Produto("P004", "Régua", 3.00, 0)
        self.assertAlmostEqual(p.valor_total(), 0.0)

    def test_preco_zero_valido(self):
        # Produto com preço zero deve ser aceito
        p = Produto("P005", "Brinde", 0.0, 10)
        self.assertAlmostEqual(p.preco, 0.0)

    def test_categoria_padrao_outro(self):
        # Categoria padrão deve ser 'outro' quando não informada
        p = Produto("P006", "Item", 5.0)
        self.assertEqual(p.categoria, "outro")

    def test_aplicar_desconto_cinquenta_por_cento(self):
        # Desconto de 50% deve retornar metade do preço original
        p = Produto("P007", "Notebook", 3000.0, 1)
        preco_com_desconto = p.aplicar_desconto(50)
        self.assertAlmostEqual(preco_com_desconto, 1500.0)

    def test_criar_produto_codigo_vazio_levanta_erro(self):
        # Código vazio deve levantar ProdutoInvalidoError
        with self.assertRaises(ProdutoInvalidoError):
            Produto("", "Produto", 5.0)

    def test_criar_produto_nome_vazio_levanta_erro(self):
        # Nome vazio deve levantar ProdutoInvalidoError
        with self.assertRaises(ProdutoInvalidoError):
            Produto("P008", "", 5.0)

    def test_criar_produto_preco_negativo_levanta_erro(self):
        # Preço negativo deve levantar ProdutoInvalidoError
        with self.assertRaises(ProdutoInvalidoError):
            Produto("P009", "Produto", -1.0)

    def test_criar_produto_quantidade_negativa_levanta_erro(self):
        # Quantidade negativa deve levantar ProdutoInvalidoError
        with self.assertRaises(ProdutoInvalidoError):
            Produto("P010", "Produto", 5.0, -10)

    def test_criar_produto_quantidade_float_levanta_erro(self):
        # Quantidade do tipo float deve levantar ProdutoInvalidoError
        with self.assertRaises(ProdutoInvalidoError):
            Produto("P011", "Produto", 5.0, 1.5)

    def test_criar_produto_categoria_invalida_levanta_erro(self):
        # Categoria inválida deve levantar CategoriaInvalidaError
        with self.assertRaises(CategoriaInvalidaError):
            Produto("P012", "Produto", 5.0, 1, "invalida")

    def test_aplicar_desconto_acima_cem_levanta_erro(self):
        # Desconto acima de 100% deve levantar ProdutoInvalidoError
        p = Produto("P013", "Produto", 100.0)
        with self.assertRaises(ProdutoInvalidoError):
            p.aplicar_desconto(101)


class TestEstoqueOperacoes(unittest.TestCase):

    def setUp(self):
        self.estoque = Estoque()
        self.produto = Produto("E001", "Caneta", 2.50, 50)
        self.estoque.adicionar_produto(self.produto)

    def test_adicionar_produto(self):
        p = Produto("E002", "Lápis", 1.00, 30)
        self.estoque.adicionar_produto(p)
        self.assertEqual(self.estoque.buscar_produto("E002"), p)

    def test_adicionar_produto_duplicado_levanta_erro(self):
        duplicado = Produto("E001", "Caneta Cópia", 3.00)
        with self.assertRaises(ProdutoInvalidoError):
            self.estoque.adicionar_produto(duplicado)

    def test_adicionar_objeto_invalido_levanta_erro(self):
        with self.assertRaises(ProdutoInvalidoError):
            self.estoque.adicionar_produto("não é produto")

    def test_remover_produto(self):
        removido = self.estoque.remover_produto("E001")
        self.assertEqual(removido.codigo, "E001")
        self.assertEqual(self.estoque.total_de_produtos(), 0)

    def test_remover_produto_inexistente_levanta_erro(self):
        with self.assertRaises(ProdutoNaoEncontradoError):
            self.estoque.remover_produto("XXXX")

    def test_buscar_produto(self):
        encontrado = self.estoque.buscar_produto("E001")
        self.assertEqual(encontrado, self.produto)

    def test_buscar_produto_codigo_minusculo_normalizado(self):
        encontrado = self.estoque.buscar_produto("e001")
        self.assertEqual(encontrado.codigo, "E001")

    def test_buscar_produto_inexistente_levanta_erro(self):
        with self.assertRaises(ProdutoNaoEncontradoError):
            self.estoque.buscar_produto("XXXX")

    def test_listar_produtos(self):
        p2 = Produto("E002", "Borracha", 0.75, 20)
        self.estoque.adicionar_produto(p2)
        lista = self.estoque.listar_produtos()
        self.assertEqual(len(lista), 2)
        self.assertIn(self.produto, lista)

    def test_entrada_aumenta_quantidade(self):
        self.estoque.entrada("E001", 10)
        self.assertEqual(self.estoque.buscar_produto("E001").quantidade, 60)

    def test_entrada_quantidade_invalida_levanta_erro(self):
        with self.assertRaises(ProdutoInvalidoError):
            self.estoque.entrada("E001", 0)

    def test_saida_diminui_quantidade(self):
        self.estoque.saida("E001", 20)
        self.assertEqual(self.estoque.buscar_produto("E001").quantidade, 30)

    def test_saida_estoque_insuficiente_levanta_erro(self):
        with self.assertRaises(EstoqueInsuficienteError):
            self.estoque.saida("E001", 100)

    def test_atualizar_preco(self):
        self.estoque.atualizar_preco("E001", 5.00)
        self.assertAlmostEqual(self.estoque.buscar_produto("E001").preco, 5.00)

    def test_atualizar_preco_negativo_levanta_erro(self):
        with self.assertRaises(ProdutoInvalidoError):
            self.estoque.atualizar_preco("E001", -1.00)

    def test_transferir_entre_estoques(self):
        destino = Estoque()
        self.estoque.transferir("E001", 15, destino)
        self.assertEqual(self.estoque.buscar_produto("E001").quantidade, 35)
        self.assertEqual(destino.buscar_produto("E001").quantidade, 15)

class TestEstoqueRelatorios(unittest.TestCase):

    def setUp(self):
        self.estoque = Estoque()
        self.p1 = Produto("R001", "Notebook", 3000.0, 2, "eletronico")
        self.p2 = Produto("R002", "Caderno", 20.0, 3, "escritorio")
        self.p3 = Produto("R003", "Arroz", 25.0, 10, "alimento")
        self.p4 = Produto("R004", "Camiseta", 50.0, 1, "vestuario")
        self.p5 = Produto("R005", "Mouse", 80.0, 0, "eletronico")

        for produto in [self.p1, self.p2, self.p3, self.p4, self.p5]:
            self.estoque.adicionar_produto(produto)

    def test_valor_total_estoque(self):
        self.assertAlmostEqual(self.estoque.valor_total_estoque(), 6360.0)

    def test_valor_total_estoque_vazio(self):
        estoque_vazio = Estoque()
        self.assertAlmostEqual(estoque_vazio.valor_total_estoque(), 0.0)

    def test_produtos_com_estoque_baixo_limite_padrao(self):
        codigos = {p.codigo for p in self.estoque.produtos_com_estoque_baixo()}
        self.assertEqual(codigos, {"R001", "R002", "R004", "R005"})

    def test_produtos_com_estoque_baixo_limite_personalizado(self):
        codigos = {p.codigo for p in self.estoque.produtos_com_estoque_baixo(2)}
        self.assertEqual(codigos, {"R004", "R005"})

    def test_produtos_com_estoque_baixo_sem_resultados(self):
        estoque_ok = Estoque()
        estoque_ok.adicionar_produto(Produto("R006", "Teclado", 100.0, 8, "eletronico"))
        self.assertEqual(estoque_ok.produtos_com_estoque_baixo(), [])

    def test_total_de_produtos(self):
        self.assertEqual(self.estoque.total_de_produtos(), 5)

    def test_total_de_produtos_estoque_vazio(self):
        self.assertEqual(Estoque().total_de_produtos(), 0)

    def test_buscar_por_categoria_retorna_produtos_corretos(self):
        codigos = {p.codigo for p in self.estoque.buscar_por_categoria("eletronico")}
        self.assertEqual(codigos, {"R001", "R005"})

    def test_buscar_por_categoria_normaliza_maiusculas_e_espacos(self):
        codigos = {p.codigo for p in self.estoque.buscar_por_categoria("  ELETRONICO ")}
        self.assertEqual(codigos, {"R001", "R005"})

    def test_buscar_por_categoria_invalida_levanta_erro(self):
        with self.assertRaises(CategoriaInvalidaError):
            self.estoque.buscar_por_categoria("brinquedo")

    def test_produto_mais_valioso(self):
        produto = self.estoque.produto_mais_valioso()
        self.assertEqual(produto.codigo, "R001")

    def test_produto_mais_valioso_estoque_vazio_levanta_erro(self):
        with self.assertRaises(ProdutoNaoEncontradoError):
            Estoque().produto_mais_valioso()

    def test_resumo_retorna_total_skus(self):
        resumo = self.estoque.resumo()
        self.assertEqual(resumo["total_skus"], 5)

    def test_resumo_retorna_total_itens(self):
        resumo = self.estoque.resumo()
        self.assertEqual(resumo["total_itens"], 16)

    def test_resumo_retorna_valor_total_e_produtos_zerados(self):
        resumo = self.estoque.resumo()
        self.assertAlmostEqual(resumo["valor_total"], 6360.0)
        self.assertEqual(resumo["produtos_zerados"], 1)


class TestEstoqueComMock(unittest.TestCase):

    def setUp(self):
        self.estoque = Estoque()
        self.produto = Produto("M001", "Monitor", 900.0, 5, "eletronico")
        self.estoque.adicionar_produto(self.produto)

    def test_transferir_chama_saida_e_adiciona_produto_no_destino(self):
        destino = Estoque()

        with patch.object(self.estoque, "saida") as mock_saida, \
             patch.object(destino, "adicionar_produto") as mock_adicionar:
            self.estoque.transferir("M001", 2, destino)

        mock_saida.assert_called_once_with("M001", 2)
        mock_adicionar.assert_called_once()

        produto_enviado = mock_adicionar.call_args[0][0]
        self.assertEqual(produto_enviado.codigo, "M001")
        self.assertEqual(produto_enviado.quantidade, 2)

    def test_transferir_para_destino_com_produto_existente_nao_chama_adicionar_produto(self):
        destino = Estoque()
        destino.adicionar_produto(Produto("M001", "Monitor", 900.0, 1, "eletronico"))

        with patch.object(self.estoque, "saida") as mock_saida, \
             patch.object(destino, "adicionar_produto") as mock_adicionar:
            self.estoque.transferir("M001", 3, destino)

        mock_saida.assert_called_once_with("M001", 3)
        mock_adicionar.assert_not_called()
        self.assertEqual(destino.buscar_produto("M001").quantidade, 4)

    def test_valor_total_estoque_soma_retorno_dos_produtos_com_mock(self):
        estoque = Estoque()

        produto1 = MagicMock()
        produto2 = MagicMock()
        produto1.valor_total.return_value = 120.0
        produto2.valor_total.return_value = 80.0

        estoque._produtos = {"A": produto1, "B": produto2}

        total = estoque.valor_total_estoque()

        self.assertEqual(total, 200.0)
        produto1.valor_total.assert_called_once()
        produto2.valor_total.assert_called_once()