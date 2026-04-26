# task-api

Uma API RESTful simples que permite criar, ler, atualizar e excluir tarefas. Pode incluir funcionalidades, entre elas marcar tarefas como concluídas e filtrar por status. A persistência dos dados pode ser feita em um banco de dados PostgreSQL.

## Objetivo

Fornecer uma micro-API leve e extensível para criação, listagem, atualização e exclusão de tarefas.

## Arquitetura

A aplicação segue uma arquitetura em camadas com separação clara de responsabilidades:

- **Frontend (React)** — interface do usuário, comunica com o backend via HTTP/JSON
- **Controller** — recebe as requisições HTTP e retorna respostas JSON
- **Service** — implementa a lógica de negócio e priorização por IA
- **Repository** — gerencia o acesso e persistência no banco de dados via SQLAlchemy ORM
- **Banco de dados (PostgreSQL)** — armazena tarefas e metadados

O diagrama de componentes completo está em [docs/architecture.md](docs/architecture.md).

## Stack

- **Python 3.13+**
- **FastAPI** — framework web
- **Pydantic** — validação de dados
- **PostgreSQL / SQLAlchemy** — persistência
- **React** — frontend
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

### v0.1 — Base da arquitetura
- [x] Estrutura de pastas: `controller`, `service`, `repository`
- [x] Conexão com PostgreSQL via SQLAlchemy
- [x] Models e migrations iniciais (tabela de tarefas)
- [x] CRUD completo: criar, listar, atualizar e excluir tarefas

### v0.2 — Funcionalidades de tarefas
- [ ] Marcar tarefas como concluídas
- [ ] Filtrar tarefas por status (pendente, concluída)
- [ ] Validação de campos com Pydantic

### v0.3 — Frontend
- [ ] Interface React para listagem e criação de tarefas
- [ ] Ações de atualizar status e excluir
- [ ] Filtro por status na interface

### v0.4 — Autenticação
- [ ] Autenticação por API key ou JWT
- [ ] Isolamento de tarefas por usuário no Repository

### v0.5 — Qualidade
- [ ] Testes por camada: controller, service e repository
- [ ] CI com GitHub Actions
- [ ] Cobertura mínima de 80%

### v1.0 — Produção
- [ ] Deploy containerizado (Docker + docker-compose)
- [ ] Variáveis de ambiente para todos os ambientes
- [ ] Documentação OpenAPI completa
