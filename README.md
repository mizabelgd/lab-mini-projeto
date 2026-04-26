# task-api

Micro-API para gestão de tarefas com priorização assistida por IA.

## Objetivo

Fornecer uma API leve e extensível para criação, listagem e priorização automática de tarefas, utilizando um modelo de linguagem para sugerir ordens de execução com base em contexto, prazo e descrição.

## Stack

- **Python 3.11+**
- **FastAPI** — framework web
- **Pydantic** — validação de dados
- **SQLite / SQLAlchemy** — persistência local
- **Claude API (Anthropic)** — priorização assistida por IA
- **Uvicorn** — servidor ASGI

## Como rodar localmente

```bash
# 1. Clone o repositório
git clone <url-do-repo>
cd task-api

# 2. Crie e ative o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# edite .env e adicione sua ANTHROPIC_API_KEY

# 5. Suba o servidor
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`.  
Documentação interativa: `http://localhost:8000/docs`

## Roadmap

### v0.1 — MVP
- [ ] CRUD de tarefas (título, descrição, prazo, status)
- [ ] Endpoint de priorização via IA
- [ ] Persistência local com SQLite

### v0.2 — Autenticação
- [ ] Autenticação por API key
- [ ] Isolamento de tarefas por usuário

### v0.3 — Qualidade
- [ ] Testes automatizados com pytest
- [ ] CI com GitHub Actions
- [ ] Cobertura mínima de 80%

### v1.0 — Produção
- [ ] Migração para PostgreSQL
- [ ] Deploy containerizado (Docker)
- [ ] Documentação OpenAPI completa
