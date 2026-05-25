# Sales Executive Dashboard

End-to-end data engineering project that extracts data from the Fake Store API, transforms and processes it, stores it in PostgreSQL, and delivers executive insights through interactive Power BI dashboards.

## Architecture

```
Fake Store API → Python ETL → PostgreSQL → Power BI Dashboard
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Extraction | Python, httpx |
| Processing | Pandas, Pydantic |
| Storage | PostgreSQL, SQLAlchemy |
| Scheduling | APScheduler |
| Visualization | Power BI |

## Project Structure

```
src/
├── config.py          # Configuration management
├── logger.py          # Centralized logging
├── extractors/        # API data extraction
├── transformers/      # Data cleaning & enrichment
├── loaders/           # PostgreSQL loading
├── models/            # SQLAlchemy ORM models
├── pipeline.py        # ETL orchestration
└── utils/             # Shared utilities
```

## Setup

1. Clone the repository
2. Copy `.env.example` to `.env` and fill in your credentials
3. Run `make dev` to install dependencies
4. Run `make run` to execute the pipeline

## License

MIT
