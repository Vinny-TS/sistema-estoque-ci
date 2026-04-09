"""
app.py – Interface Web do Sistema de Estoque
Execute com:  python app.py
Acesse em:   http://127.0.0.1:5000
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from src.estoque import (
    Estoque, Produto,
    ProdutoInvalidoError, EstoqueInsuficienteError,
    ProdutoNaoEncontradoError, CategoriaInvalidaError,
    CATEGORIAS_VALIDAS,
)

app = Flask(__name__)
app.secret_key = "estoque-c14-inatel"

# ── Estado em memória (persiste enquanto o servidor roda) ─────────────────────
estoque = Estoque()

# Produtos de exemplo para demonstração
_exemplos = [
    ("NB001", "Notebook Dell",    3_499.90, 12, "eletronico"),
    ("MS001", "Mouse Logitech",      89.90, 45, "eletronico"),
    ("CA001", "Caneta BIC (cx50)",    8.50, 200,"escritorio"),
    ("CH001", "Camiseta Polo",        59.90,  8, "vestuario"),
    ("PA001", "Pão Integral",          6.90, 30, "alimento"),
]
for _args in _exemplos:
    try:
        estoque.adicionar_produto(Produto(*_args))
    except Exception:
        pass


# ── Rotas ─────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    produtos = estoque.listar_produtos()
    resumo   = estoque.resumo()
    baixo    = estoque.produtos_com_estoque_baixo(limite=10)
    categorias = sorted(CATEGORIAS_VALIDAS)
    return render_template("index.html",
                           produtos=produtos,
                           resumo=resumo,
                           baixo=baixo,
                           categorias=categorias)


@app.route("/adicionar", methods=["POST"])
def adicionar():
    try:
        p = Produto(
            request.form["codigo"],
            request.form["nome"],
            float(request.form["preco"]),
            int(request.form["quantidade"]),
            request.form.get("categoria", "outro"),
        )
        estoque.adicionar_produto(p)
        flash(f"Produto '{p.nome}' adicionado com sucesso!", "success")
    except (ProdutoInvalidoError, CategoriaInvalidaError, ValueError) as e:
        flash(str(e), "error")
    return redirect(url_for("index"))


@app.route("/remover/<codigo>", methods=["POST"])
def remover(codigo):
    try:
        p = estoque.remover_produto(codigo)
        flash(f"Produto '{p.nome}' removido.", "warning")
    except ProdutoNaoEncontradoError as e:
        flash(str(e), "error")
    return redirect(url_for("index"))


@app.route("/entrada", methods=["POST"])
def entrada():
    try:
        codigo = request.form["codigo"]
        qtd    = int(request.form["quantidade"])
        estoque.entrada(codigo, qtd)
        p = estoque.buscar_produto(codigo)
        flash(f"+{qtd} unidades em '{p.nome}'. Estoque atual: {p.quantidade}", "success")
    except (ProdutoInvalidoError, ProdutoNaoEncontradoError, ValueError) as e:
        flash(str(e), "error")
    return redirect(url_for("index"))


@app.route("/saida", methods=["POST"])
def saida():
    try:
        codigo = request.form["codigo"]
        qtd    = int(request.form["quantidade"])
        p      = estoque.buscar_produto(codigo)
        estoque.saida(codigo, qtd)
        flash(f"-{qtd} unidades de '{p.nome}'. Estoque atual: {p.quantidade}", "success")
    except (ProdutoInvalidoError, EstoqueInsuficienteError,
            ProdutoNaoEncontradoError, ValueError) as e:
        flash(str(e), "error")
    return redirect(url_for("index"))


@app.route("/atualizar_preco", methods=["POST"])
def atualizar_preco():
    try:
        codigo = request.form["codigo"]
        preco  = float(request.form["preco"])
        estoque.atualizar_preco(codigo, preco)
        p = estoque.buscar_produto(codigo)
        flash(f"Preço de '{p.nome}' atualizado para R$ {preco:.2f}", "success")
    except (ProdutoInvalidoError, ProdutoNaoEncontradoError, ValueError) as e:
        flash(str(e), "error")
    return redirect(url_for("index"))


@app.route("/api/produtos")
def api_produtos():
    """Endpoint JSON com todos os produtos (bônus)."""
    return jsonify([
        {"codigo": p.codigo, "nome": p.nome, "preco": p.preco,
         "quantidade": p.quantidade, "categoria": p.categoria,
         "valor_total": p.valor_total()}
        for p in estoque.listar_produtos()
    ])


if __name__ == "__main__":
    app.run(debug=True)
