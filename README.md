# Dashboard Executivo de Vendas

Projeto completo de engenharia de dados que extrai dados da Fake Store API, transforma e processa, armazena em PostgreSQL e entrega insights executivos através de dashboards interativos no Power BI.

## Arquitetura

```
Fake Store API → Python ETL → PostgreSQL → Power BI Dashboard
```

## Stack Tecnológico

| Camada | Tecnologia |
|--------|-----------|
| Extração | Python, httpx |
| Processamento | Pandas, Pydantic |
| Armazenamento | PostgreSQL, SQLAlchemy |
| Agendamento | APScheduler |
| Visualização | Power BI |

## Estrutura do Projeto

```
src/
├── config.py          # Gerenciamento de configuração
├── logger.py          # Logging centralizado
├── extractors/        # Extração de dados da API
├── transformers/      # Limpeza e enriquecimento de dados
├── loaders/           # Carregamento no PostgreSQL
├── models/            # Modelos ORM SQLAlchemy
├── pipeline.py        # Orquestração ETL
└── utils/             # Utilitários compartilhados
```

## Setup

1. Clone o repositório
2. Copie `.env.example` para `.env` e preencha suas credenciais
3. Execute `make dev` para instalar as dependências
4. Execute `make run` para executar o pipeline

## Licença

MIT
