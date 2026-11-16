# healthOps

API para consulta de estabelecimentos de saúde (UBSs, hospitais, clínicas etc.), construída com **FastAPI** e **PostgreSQL**.

> Projeto em estágio inicial.

## Tecnologias

- Python 3.10+
- [FastAPI](https://fastapi.tiangolo.com/) + Uvicorn
- [psycopg 3](https://www.psycopg.org/psycopg3/) com `psycopg_pool` (pool de conexões)
- Pydantic (schemas de resposta)
- python-dotenv (variáveis de ambiente)
- PostgreSQL 17 via Docker Compose

## Estrutura

```
healthOps/
├── .venv/                    # Ambiente virtual Python (não versionado)
├── .env.example              # Modelo das variáveis de ambiente
├── .gitignore
├── compose.yaml              # Container do PostgreSQL
├── requirements.txt          # Dependências Python
├── README.md
└── backend/
    ├── conexao.py            # Script avulso para testar a conexão com o banco
    └── app/
        ├── main.py           # Instância do FastAPI, lifespan do pool, / e /api/health
        ├── database.py       # Configuração do banco (DB_CONFIG) e pool de conexões
        ├── schemas.py        # Modelos Pydantic
        ├── repositories/
        │   └── estabelecimentos.py   # Consultas SQL de estabelecimentos
        └── routers/
            └── estabelecimentos.py   # Rotas de /api/estabelecimentos
```

## Configuração

### 1. Variáveis de ambiente

Copie o modelo e ajuste os valores:

```bash
cp .env.example .env
```

| Variável            | Usada por        | Descrição                                     |
|---------------------|------------------|-----------------------------------------------|
| `POSTGRES_USER`     | Compose e API    | Usuário do banco                              |
| `POSTGRES_PASSWORD` | Compose e API    | Senha do banco                                |
| `POSTGRES_DB`       | Compose e API    | Nome do banco                                 |
| `POSTGRES_HOST`     | API              | Host do banco (padrão: `localhost`)           |
| `POSTGRES_PORT`     | Compose e API    | Porta exposta no host (padrão: `5433`)        |

O `.env` fica na raiz do projeto e não é versionado.

### 2. Banco de dados

```bash
docker compose up -d
```

Os dados ficam persistidos no volume `postgres_data`.

> **Atenção:** o Postgres só lê `POSTGRES_USER`, `POSTGRES_PASSWORD` e `POSTGRES_DB` na **primeira** criação do volume. Se você alterar esses valores depois (por exemplo, ao migrar do nome antigo do projeto), recrie o volume com `docker compose down -v && docker compose up -d` — isso **apaga todos os dados** — ou crie o novo usuário/banco manualmente.

A tabela `estabelecimentos` precisa existir no banco; os campos esperados pela API são:

| Coluna      | Tipo    | Obrigatório |
|-------------|---------|-------------|
| `id`        | integer | sim         |
| `nome`      | text    | sim         |
| `municipio` | text    | sim         |
| `tipo`      | text    | não         |
| `ativo`     | boolean | não         |

Para acessar o banco pelo terminal:

```bash
docker exec -it healthops-db psql -U <POSTGRES_USER> -d <POSTGRES_DB>
```

#### Criando a tabela `estabelecimentos`

Com o `psql` aberto (comando acima), execute:

```sql
CREATE TABLE IF NOT EXISTS estabelecimentos (
    id        SERIAL PRIMARY KEY,
    nome      TEXT    NOT NULL,
    municipio TEXT    NOT NULL,
    tipo      TEXT,
    ativo     BOOLEAN DEFAULT TRUE
);

-- Índice para as consultas por município
CREATE INDEX IF NOT EXISTS idx_estabelecimentos_municipio
    ON estabelecimentos (municipio);
```

Opcionalmente, insira alguns dados de exemplo:

```sql
INSERT INTO estabelecimentos (nome, municipio, tipo, ativo) VALUES
    ('UBS Central',        'São Paulo',      'Unidade Básica de Saúde', TRUE),
    ('Hospital Municipal', 'Campinas',       'Hospital',                TRUE),
    ('Clínica Bem-Estar',  'Rio de Janeiro', 'Clínica',                 FALSE);
```

Confira o resultado com `SELECT * FROM estabelecimentos;` e saia do `psql` com `\q`.

Também é possível executar o SQL sem entrar no `psql`, salvando os comandos em um arquivo (por exemplo, `schema.sql`) e rodando:

```bash
docker exec -i healthops-db psql -U <POSTGRES_USER> -d <POSTGRES_DB> < schema.sql
```

### 3. Ambiente Python

O ambiente virtual fica na raiz do projeto (`healthOps/.venv`). A partir da raiz:

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Executando a API

Com o ambiente virtual ativado, a partir da pasta `backend/`:

```bash
cd backend
uvicorn app.main:app --reload
```

A API sobe em `http://localhost:8000`. A documentação interativa fica em:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

| Método | Rota                    | Descrição                       |
|--------|-------------------------|---------------------------------|
| GET    | `/`                     | Mensagem de boas-vindas         |
| GET    | `/api/health`           | Verifica se a API está no ar    |
| GET    | `/api/estabelecimentos` | Lista todos os estabelecimentos |

Exemplo de resposta de `/api/estabelecimentos`:

```json
[
  {
    "id": 1,
    "nome": "UBS Central",
    "municipio": "São Paulo",
    "tipo": "Unidade Básica de Saúde",
    "ativo": true
  }
]
```

## Testando a conexão sem a API

```bash
cd backend
python conexao.py
```

O script usa a mesma configuração da API (`DB_CONFIG`) e imprime as linhas da tabela `estabelecimentos`.
