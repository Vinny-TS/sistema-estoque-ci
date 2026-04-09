import unittest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.estoque import (
    Produto,
    ProdutoInvalidoError,
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