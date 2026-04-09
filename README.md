# 📦 Sistema de Estoque – CI/CD Pipeline

[![CI/CD](https://github.com/Vinny-TS/sistema-estoque-ci/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Vinny-TS/sistema-estoque-ci/actions/workflows/ci-cd.yml)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> Projeto desenvolvido para a disciplina **C14 – Engenharia de Software**  
> Instituto Nacional de Telecomunicações – **Inatel**  
> Professor: Christopher Lima

---

## 🎯 Sobre o Projeto

Sistema de gerenciamento de estoque desenvolvido em Python, com interface web (Flask) e pipeline completo de CI/CD via GitHub Actions.

O sistema permite cadastrar produtos com categoria, registrar entradas e saídas, atualizar preços, transferir itens entre estoques e visualizar relatórios — tudo acessível por uma interface web local ou pela API JSON.

---

## ✨ Funcionalidades

- Cadastro, busca, listagem e remoção de produtos
- Categorias: `eletronico`, `escritorio`, `alimento`, `vestuario`, `outro`
- Registro de entradas e saídas de estoque
- Transferência de itens entre estoques
- Atualização de preços e aplicação de descontos
- Relatório de valor total, produtos com estoque baixo e resumo geral
- Interface web com dashboard de KPIs e alertas
- API JSON em `/api/produtos`

---

## 🗂️ Estrutura do Projeto

```
sistema-estoque-ci/
├── src/
│   ├── __init__.py
│   └── estoque.py           # Lógica principal (Produto, Estoque, exceções)
├── tests/
│   ├── __init__.py
│   └── test_estoque.py      # Testes unitários
├── templates/
│   └── index.html           # Interface web (Flask)
├── scripts/
│   └── notificar.py         # Notificação por e-mail ao fim do pipeline
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # Pipeline GitHub Actions
├── app.py                   # Servidor web Flask
├── requirements.txt
├── setup.py
├── .gitignore
└── README.md
```

---

## 🚀 Como Rodar Localmente

```bash
# 1. Clone o repositório
git clone https://github.com/Vinny-TS/sistema-estoque-ci.git
cd sistema-estoque-ci

# 2. Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate    # Linux/macOS
.venv\Scripts\activate       # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Suba a interface web
python app.py

# 5. Acesse no navegador
#    http://127.0.0.1:5000
```

---

## 🔄 Pipeline CI/CD

O pipeline é executado automaticamente a cada `push` ou `pull_request` na branch `main`.

```
testes ──┬──> build ──> deploy (GitHub Release)
          └──> notificacao  (paralelo ao build)
```

| Job | Descrição | Condição |
|-----|-----------|----------|
| 🧪 **testes** | Executa todos os testes unitários com relatório de cobertura | Sempre |
| 📦 **build** | Gera pacote `.whl` e `.tar.gz` | Após testes passarem |
| 📧 **notificacao** | Envia e-mail com o resultado do pipeline | Paralelo ao build, sempre |
| 🚀 **deploy** | Publica GitHub Release com o pacote gerado | Apenas em push na `main` |

**Artefatos armazenados no GitHub Actions:**
- `relatorio-testes/` → `junit.xml` e `coverage.xml`
- `pacote-distribuivel/` → `.whl` e `.tar.gz`

---

## ⚙️ Configuração dos Secrets

Para que a notificação por e-mail funcione, configure os seguintes **Secrets** no repositório:

> **Settings → Secrets and variables → Actions → New repository secret**

| Secret | Descrição |
|--------|-----------|
| `SMTP_USER` | E-mail do remetente (Gmail) |
| `SMTP_PASSWORD` | Senha de app do Gmail ([como gerar](https://support.google.com/accounts/answer/185833)) |
| `NOTIFY_EMAIL` | E-mail que receberá as notificações do pipeline |

> ⚠️ Nenhum endereço de e-mail está fixado no código — todos são lidos exclusivamente via Secrets/variáveis de ambiente.

---

## 🤖 Uso de IA

Este projeto utilizou IA (Claude – Anthropic) como auxílio na estruturação inicial do código, testes e pipeline.

Os prompts principais foram:

1. *"Monte um sistema de estoque em Python com classes Produto e Estoque, com validações, categorias, transferência entre estoques e relatórios."*
2. *"Crie testes unitários cobrindo fluxo normal e de extensão, incluindo mocks com MagicMock."*
3. *"Crie um workflow GitHub Actions com 4 jobs (testes, build, notificação e deploy), sendo build e notificação paralelos, com artefatos e deploy via GitHub Releases."*
4. *"Crie uma interface web com Flask e um template HTML com visual industrial para o sistema de estoque."*

O resultado foi **satisfatório** e serviu como ponto de partida, sendo revisado e adaptado pelo grupo.

---

## 👥 Integrantes

| Nome | GitHub |
|------|--------|
| Vinicius Telles | [@Vinny-TS](https://github.com/Vinny-TS) |
| Matheus de Alencar | [@titiomathias](https://github.com/titiomathias) |
| Vinicius de Souza | [@viniss211](https://github.com/viniss211) |

---

## 📄 Licença

Distribuído sob a licença MIT.
