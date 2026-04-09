"""
Sistema de Estoque - Módulo Principal
Gerencia produtos, quantidades, preços, categorias e relatórios de estoque.
"""


class ProdutoInvalidoError(Exception):
    """Exceção para produto com dados inválidos."""
    pass


class EstoqueInsuficienteError(Exception):
    """Exceção para operações com estoque insuficiente."""
    pass


class ProdutoNaoEncontradoError(Exception):
    """Exceção para produto não encontrado no estoque."""
    pass


class CategoriaInvalidaError(Exception):
    """Exceção para categoria inválida."""
    pass


# Categorias válidas do sistema
CATEGORIAS_VALIDAS = {"eletronico", "escritorio", "alimento", "vestuario", "outro"}


class Produto:
    """Representa um produto no sistema de estoque."""

    def __init__(
        self,
        codigo: str,
        nome: str,
        preco: float,
        quantidade: int = 0,
        categoria: str = "outro",
    ):
        if not codigo or not isinstance(codigo, str):
            raise ProdutoInvalidoError("Código do produto inválido.")
        if not nome or not isinstance(nome, str):
            raise ProdutoInvalidoError("Nome do produto inválido.")
        if not isinstance(preco, (int, float)) or preco < 0:
            raise ProdutoInvalidoError("Preço deve ser um número não negativo.")
        if not isinstance(quantidade, int) or quantidade < 0:
            raise ProdutoInvalidoError("Quantidade deve ser um inteiro não negativo.")
        categoria_norm = categoria.strip().lower()
        if categoria_norm not in CATEGORIAS_VALIDAS:
            raise CategoriaInvalidaError(
                f"Categoria '{categoria}' inválida. Use: {sorted(CATEGORIAS_VALIDAS)}"
            )

        self.codigo = codigo.strip().upper()
        self.nome = nome.strip()
        self.preco = float(preco)
        self.quantidade = quantidade
        self.categoria = categoria_norm

    def __repr__(self):
        return (
            f"Produto(codigo={self.codigo!r}, nome={self.nome!r}, "
            f"preco={self.preco}, quantidade={self.quantidade}, "
            f"categoria={self.categoria!r})"
        )

    def valor_total(self) -> float:
        """Retorna o valor total do produto em estoque (preço × quantidade)."""
        return round(self.preco * self.quantidade, 2)

    def aplicar_desconto(self, percentual: float) -> float:
        """Retorna o preço após aplicar um desconto percentual (0–100)."""
        if not isinstance(percentual, (int, float)) or not (0 <= percentual <= 100):
            raise ProdutoInvalidoError("Percentual de desconto deve estar entre 0 e 100.")
        return round(self.preco * (1 - percentual / 100), 2)


class Estoque:
    """Gerencia o conjunto de produtos em estoque."""

    def __init__(self):
        self._produtos: dict[str, Produto] = {}

    # ──────────────────────────────────────────────
    # Operações CRUD
    # ──────────────────────────────────────────────

    def adicionar_produto(self, produto: Produto) -> None:
        """Adiciona um novo produto ao estoque."""
        if not isinstance(produto, Produto):
            raise ProdutoInvalidoError("Objeto não é uma instância de Produto.")
        if produto.codigo in self._produtos:
            raise ProdutoInvalidoError(f"Produto com código '{produto.codigo}' já existe.")
        self._produtos[produto.codigo] = produto

    def remover_produto(self, codigo: str) -> Produto:
        """Remove e retorna um produto do estoque pelo código."""
        codigo = codigo.strip().upper()
        if codigo not in self._produtos:
            raise ProdutoNaoEncontradoError(f"Produto '{codigo}' não encontrado.")
        return self._produtos.pop(codigo)

    def buscar_produto(self, codigo: str) -> Produto:
        """Retorna um produto pelo código."""
        codigo = codigo.strip().upper()
        if codigo not in self._produtos:
            raise ProdutoNaoEncontradoError(f"Produto '{codigo}' não encontrado.")
        return self._produtos[codigo]

    def listar_produtos(self) -> list[Produto]:
        """Retorna lista de todos os produtos."""
        return list(self._produtos.values())

    # ──────────────────────────────────────────────
    # Movimentações
    # ──────────────────────────────────────────────

    def entrada(self, codigo: str, quantidade: int) -> None:
        """Registra entrada (compra/recebimento) de itens no estoque."""
        if not isinstance(quantidade, int) or quantidade <= 0:
            raise ProdutoInvalidoError("Quantidade de entrada deve ser inteiro positivo.")
        produto = self.buscar_produto(codigo)
        produto.quantidade += quantidade

    def saida(self, codigo: str, quantidade: int) -> None:
        """Registra saída (venda/consumo) de itens do estoque."""
        if not isinstance(quantidade, int) or quantidade <= 0:
            raise ProdutoInvalidoError("Quantidade de saída deve ser inteiro positivo.")
        produto = self.buscar_produto(codigo)
        if produto.quantidade < quantidade:
            raise EstoqueInsuficienteError(
                f"Estoque insuficiente para '{produto.nome}': "
                f"disponível={produto.quantidade}, solicitado={quantidade}."
            )
        produto.quantidade -= quantidade

    def atualizar_preco(self, codigo: str, novo_preco: float) -> None:
        """Atualiza o preço de um produto."""
        if not isinstance(novo_preco, (int, float)) or novo_preco < 0:
            raise ProdutoInvalidoError("Novo preço deve ser um número não negativo.")
        produto = self.buscar_produto(codigo)
        produto.preco = float(novo_preco)

    def transferir(self, codigo: str, quantidade: int, destino: "Estoque") -> None:
        """Transfere itens de um estoque para outro."""
        if not isinstance(destino, Estoque):
            raise ProdutoInvalidoError("Destino deve ser uma instância de Estoque.")
        # Valida e debita no estoque origem
        self.saida(codigo, quantidade)
        produto_origem = self.buscar_produto(codigo)
        # Credita no destino
        if codigo in destino._produtos:
            destino._produtos[codigo].quantidade += quantidade
        else:
            novo = Produto(
                produto_origem.codigo,
                produto_origem.nome,
                produto_origem.preco,
                quantidade,
                produto_origem.categoria,
            )
            destino.adicionar_produto(novo)

    # ──────────────────────────────────────────────
    # Relatórios
    # ──────────────────────────────────────────────

    def valor_total_estoque(self) -> float:
        """Retorna o valor total de todos os produtos em estoque."""
        return round(sum(p.valor_total() for p in self._produtos.values()), 2)

    def produtos_com_estoque_baixo(self, limite: int = 5) -> list[Produto]:
        """Retorna produtos com quantidade abaixo do limite."""
        return [p for p in self._produtos.values() if p.quantidade < limite]

    def total_de_produtos(self) -> int:
        """Retorna o número de SKUs cadastrados."""
        return len(self._produtos)

    def buscar_por_categoria(self, categoria: str) -> list[Produto]:
        """Retorna todos os produtos de uma determinada categoria."""
        categoria_norm = categoria.strip().lower()
        if categoria_norm not in CATEGORIAS_VALIDAS:
            raise CategoriaInvalidaError(
                f"Categoria '{categoria}' inválida. Use: {sorted(CATEGORIAS_VALIDAS)}"
            )
        return [p for p in self._produtos.values() if p.categoria == categoria_norm]

    def produto_mais_valioso(self) -> Produto:
        """Retorna o produto com maior valor total em estoque."""
        if not self._produtos:
            raise ProdutoNaoEncontradoError("Estoque vazio.")
        return max(self._produtos.values(), key=lambda p: p.valor_total())

    def resumo(self) -> dict:
        """Retorna um dicionário com métricas gerais do estoque."""
        produtos = list(self._produtos.values())
        return {
            "total_skus": len(produtos),
            "total_itens": sum(p.quantidade for p in produtos),
            "valor_total": self.valor_total_estoque(),
            "produtos_zerados": sum(1 for p in produtos if p.quantidade == 0),
        }
