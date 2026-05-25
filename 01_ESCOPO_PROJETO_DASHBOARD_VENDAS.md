# 📊 ESCOPO DO PROJETO: DASHBOARD EXECUTIVO DE VENDAS

**Versão:** 1.0  
**Data:** Maio 2026  
**Autor:** Seu Nome  
**Status:** Planejamento  

---

## 1. VISÃO GERAL DO PROJETO

### 1.1 Objetivo Geral
Desenvolver uma solução completa de engenharia de dados (end-to-end) que extrai dados de uma API de e-commerce, processa, armazena em banco de dados relacional e apresenta insights executivos através de um dashboard interativo no Power BI.

### 1.2 Contexto
- **Fonte de Dados:** Fake Store API (API REST gratuita com dados sintéticos de e-commerce)
- **Objetivo Final:** Dashboard Executivo para análise de vendas, produtos e comportamento de clientes
- **Público-alvo:** Executivos e gestores de vendas
- **Stack Tecnológico:** Python | PostgreSQL | Power BI

### 1.3 Principais Benefícios
✅ Demonstrar habilidades completas em Data Engineering  
✅ Portfolio com projeto real e escalável  
✅ Boas práticas de código, versionamento e documentação  
✅ Solução reproduzível e mantível  

---

## 2. ESCOPO DETALHADO

### 2.1 Fases do Projeto

#### **FASE 1: DESCOBERTA E PLANEJAMENTO** (1 semana)
- [ ] Análise da documentação da API
- [ ] Mapeamento de endpoints e estrutura de dados
- [ ] Desenho do modelo de dados (ERD)
- [ ] Definição de arquitetura
- [ ] Setup do ambiente de desenvolvimento

#### **FASE 2: EXTRAÇÃO DE DADOS (DATA INGESTION)** (2 semanas)
- [ ] Implementar scripts de coleta de dados (ETL)
- [ ] Tratamento de erros e validações
- [ ] Implementar estratégias de sincronização incremental
- [ ] Logging e monitoramento
- [ ] Testes unitários

#### **FASE 3: TRANSFORMAÇÃO E LIMPEZA (DATA PROCESSING)** (2 semanas)
- [ ] Limpeza e validação de dados
- [ ] Enriquecimento de dados
- [ ] Cálculo de métricas e agregações
- [ ] Tratamento de duplicatas e anomalias
- [ ] Testes de qualidade de dados

#### **FASE 4: ARMAZENAMENTO (DATA WAREHOUSE)** (1 semana)
- [ ] Setup do PostgreSQL
- [ ] Criação do schema e tabelas
- [ ] Índices e otimizações
- [ ] Implementar política de retenção de dados
- [ ] Testes de integridade referencial

#### **FASE 5: VISUALIZAÇÃO (BI & REPORTING)** (2 semanas)
- [ ] Conexão Power BI com PostgreSQL
- [ ] Criação de modelos semânticos
- [ ] Desenvolvimento de dashboards
- [ ] Validação de métricas e KPIs
- [ ] Testes de performance

#### **FASE 6: DOCUMENTAÇÃO E DEPLOY** (1 semana)
- [ ] Documentação técnica completa
- [ ] Guia de usuário
- [ ] Plano de manutenção
- [ ] Preparação para portfolio

---

## 3. ESTRUTURA TÉCNICA

### 3.1 Arquitetura da Solução

```
┌─────────────────────────────────────────────────────┐
│           FAKE STORE API (Fonte)                    │
│  (Products, Carts, Orders, Users, Categories)      │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│     CAMADA DE EXTRAÇÃO (Python)                     │
│  • API Connector                                    │
│  • Request Handler                                  │
│  • Error Management                                 │
│  • Data Validation                                  │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│     CAMADA DE TRANSFORMAÇÃO (Python)                │
│  • Data Cleaning                                    │
│  • Data Enrichment                                  │
│  • Business Rules                                   │
│  • Quality Checks                                   │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│     CAMADA DE ARMAZENAMENTO                         │
│  PostgreSQL Database                                │
│  • Staging Layer                                    │
│  • Warehouse Layer                                  │
│  • Mart Layer                                       │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│     CAMADA DE VISUALIZAÇÃO                          │
│  Power BI Desktop/Service                           │
│  • Executive Dashboard                              │
│  • Sales KPIs                                       │
│  • Interative Reports                               │
└─────────────────────────────────────────────────────┘
```

### 3.2 Stack Tecnológico Detalhado

| Componente | Tecnologia | Versão | Função |
|-----------|-----------|--------|--------|
| **Extração** | Python 3.11+ | Latest | Coleta de dados da API |
| **Processamento** | Pandas | 2.x | Transformação de dados |
| **Validação** | Great Expectations | 0.18+ | Qualidade de dados |
| **BD Relacional** | PostgreSQL | 14+ | Armazenamento persistente |
| **ORM** | SQLAlchemy | 2.0+ | Abstração de BD |
| **Scheduling** | APScheduler | 3.10+ | Automação de jobs |
| **Logging** | Python logging | Built-in | Rastreabilidade |
| **Testing** | Pytest | 7.x | Testes unitários |
| **BI** | Power BI Desktop | Latest | Visualização final |

---

## 4. MODELO DE DADOS

### 4.1 Dimensões e Fatos

#### **Tabelas de Dimensão (Conformed)**
- **dim_products:** ID, Nome, Categoria, Preço, Descrição, Ativo
- **dim_categories:** ID, Nome, Descrição
- **dim_users:** ID, Nome, Email, Telefone, País, Cidade, CEP
- **dim_dates:** Data, Ano, Mês, Trimestre, Dia da Semana, Semana

#### **Tabelas de Fato (Transacional)**
- **fct_sales:** ID_Venda, ID_Produto, ID_Usuário, ID_Data, Quantidade, Preço_Unitário, Valor_Total, Desconto
- **fct_carts:** ID_Carrinho, ID_Usuário, ID_Data, Valor_Total, Data_Criação

#### **Tabelas de Staging (Raw)**
- **stg_api_products:** Dados brutos da API
- **stg_api_carts:** Dados brutos da API
- **stg_api_users:** Dados brutos da API

### 4.2 Schema ERD (Conceitual)

```
┌──────────────────┐
│   dim_products   │
├──────────────────┤
│ product_id (PK)  │
│ product_name     │
│ category_id (FK) │
│ price            │
│ description      │
│ is_active        │
└──────────────────┘
         │ 1:N
         │
         ├─────────────────────┐
         │                     │
         ▼                     ▼
┌──────────────────┐   ┌──────────────────┐
│   dim_categories │   │   fct_sales      │
├──────────────────┤   ├──────────────────┤
│ category_id (PK) │   │ sale_id (PK)     │
│ category_name    │   │ product_id (FK)  │
│ description      │   │ user_id (FK)     │
└──────────────────┘   │ date_id (FK)     │
                       │ quantity         │
                       │ unit_price       │
                       │ total_amount     │
                       │ discount         │
                       └──────────────────┘
                              │ N:1
                              │
                       ┌──────────────────┐
                       │   dim_users      │
                       ├──────────────────┤
                       │ user_id (PK)     │
                       │ user_name        │
                       │ email            │
                       │ phone            │
                       │ country          │
                       │ city             │
                       │ postal_code      │
                       └──────────────────┘
                              │ N:1
                              │
                       ┌──────────────────┐
                       │   dim_dates      │
                       ├──────────────────┤
                       │ date_id (PK)     │
                       │ date             │
                       │ year             │
                       │ month            │
                       │ quarter          │
                       │ day_of_week      │
                       │ week_of_year     │
                       └──────────────────┘
```

---

## 5. ENDPOINTS DA API

### 5.1 Estrutura de Dados Esperados

#### **Produtos**
```
GET /products
GET /products/:id
GET /products/categories
GET /products/category/:category
```
**Campos:** id, title, price, description, category, image, rating

#### **Carrinhos**
```
GET /carts
GET /carts/:id
GET /carts/user/:userId
```
**Campos:** id, userId, date, products (com id e quantity)

#### **Usuários**
```
GET /users
GET /users/:id
```
**Campos:** id, username, email, address, phone, website

#### **Limitações Conhecidas**
- API não possui endpoint de pedidos/vendas diretos
- Dados são sintéticos e estáticos
- Sem autenticação requerida

---

## 6. KPIs E MÉTRICAS EXECUTIVAS

### 6.1 Métricas Principais do Dashboard

| KPI | Fórmula | Dimensão | Frequência |
|-----|---------|----------|-----------|
| **Revenue Total** | SUM(fct_sales.total_amount) | Mensal/Anual | Diária |
| **Número de Transações** | COUNT(fct_sales.sale_id) | Mensal | Diária |
| **Ticket Médio** | AVG(fct_sales.total_amount) | Mensal | Semanal |
| **Quantidade Vendida** | SUM(fct_sales.quantity) | Categoria | Diária |
| **Produto Top Seller** | MAX(SUM(quantity)) by produto | N/A | Semanal |
| **Categoria Mais Lucrativa** | SUM(total_amount) by categoria | Anual | Semanal |
| **Taxa de Desconto Médio** | AVG(discount) | Geral | Mensal |
| **Número de Clientes Ativos** | COUNT(DISTINCT user_id) | Geral | Mensal |
| **Crescimento MoM** | ((Current Month - Previous Month) / Previous Month) * 100 | Mensal | Mensal |

### 6.2 Dashboards Propostos

1. **Dashboard Executivo (Página 1)**
   - KPIs principais em cards
   - Trend de vendas (linha) últimos 12 meses
   - Top 10 produtos por receita
   - Distribuição por categoria (pizza)

2. **Dashboard Detalhado (Página 2)**
   - Vendas por período (calendário de calor)
   - Performance por categoria (barras)
   - Top clientes por valor (tabela)
   - Análise de tickets (histograma)

3. **Dashboard Analítico (Página 3)**
   - Correlação produtos x categorias
   - Segmentação de clientes
   - Sazonalidade de vendas
   - Previsões (tendência)

---

## 7. BOAS PRÁTICAS IMPLEMENTADAS

### 7.1 Código e Arquitetura

- ✅ **Estrutura de Projeto Profissional**
  ```
  projeto_sales_dashboard/
  ├── .git/
  ├── .gitignore
  ├── README.md
  ├── requirements.txt
  ├── setup.py
  ├── .env.example
  ├── Makefile
  ├── docs/
  │   ├── ARQUITETURA.md
  │   ├── API_MAPPING.md
  │   └── GUIA_USUARIO.md
  ├── src/
  │   ├── __init__.py
  │   ├── config.py
  │   ├── logger.py
  │   ├── extractors/
  │   │   ├── __init__.py
  │   │   ├── base_extractor.py
  │   │   ├── api_client.py
  │   │   └── fake_store_extractor.py
  │   ├── transformers/
  │   │   ├── __init__.py
  │   │   ├── base_transformer.py
  │   │   ├── data_cleaner.py
  │   │   ├── data_enricher.py
  │   │   └── validators.py
  │   ├── loaders/
  │   │   ├── __init__.py
  │   │   ├── database.py
  │   │   └── postgres_loader.py
  │   ├── models/
  │   │   ├── __init__.py
  │   │   ├── staging.py
  │   │   └── warehouse.py
  │   ├── pipeline.py
  │   └── utils/
  │       ├── __init__.py
  │       ├── validators.py
  │       └── helpers.py
  ├── tests/
  │   ├── __init__.py
  │   ├── test_extractors.py
  │   ├── test_transformers.py
  │   ├── test_loaders.py
  │   └── conftest.py
  ├── notebooks/
  │   ├── 01_exploracao_api.ipynb
  │   ├── 02_analise_dados.ipynb
  │   └── 03_validacoes.ipynb
  ├── scripts/
  │   ├── init_database.py
  │   ├── run_pipeline.py
  │   └── scheduler.py
  └── dashboards/
      └── sales_dashboard.pbix
  ```

- ✅ **Versionamento**
  - Git com commits semânticos
  - Branches (main, develop, feature/*)
  - Tags para releases

- ✅ **Código Limpo**
  - Type hints em todas as funções
  - Docstrings (Google style)
  - PEP 8 compliance
  - Máximo de 80-100 caracteres por linha

- ✅ **Testing**
  - Cobertura mínima de 80%
  - Testes unitários para cada módulo
  - Testes de integração
  - Testes de validação de dados

### 7.2 Dados e Qualidade

- ✅ **Validações**
  - Schema validation na ingestão
  - Data type checking
  - Range validation (preços, quantidades)
  - Null/Missing values handling
  - Duplicate detection

- ✅ **Data Quality Checks**
  - Comparação antes/depois transformação
  - Alertas para anomalias
  - Logs de rejeição de registros
  - SLA de dados (completude, acurácia)

- ✅ **Rastreabilidade**
  - Audit trail (quem, quando, o quê)
  - Lineage de dados
  - Versionamento de dados

### 7.3 Segurança

- ✅ **Gestão de Credenciais**
  - Variáveis de ambiente (.env)
  - Nunca commit de senhas
  - Exemplo de .env.example
  - Secrets management

- ✅ **Acesso ao Banco**
  - Connection pooling
  - SSL/TLS para BD
  - Least privilege principle
  - Backup automático

### 7.4 Performance

- ✅ **Otimizações**
  - Índices nas FK e PKs
  - Batch processing
  - Connection pooling
  - Queries otimizadas

- ✅ **Monitoramento**
  - Tempo de execução de jobs
  - Tamanho das tabelas
  - Uso de recursos

### 7.5 Documentação

- ✅ **Documentação Técnica**
  - README completo
  - Guia de instalação
  - Documentação de API interna
  - Diagrama de arquitetura
  - Dicionário de dados

- ✅ **Documentação de Negócio**
  - Glossário de termos
  - Dicionário de dados (técnico + negócio)
  - Manual de KPIs
  - Guia do usuário Power BI

---

## 8. CRONOGRAMA E ESFORÇO

| Fase | Duração | Esforço | Deliverables |
|------|---------|--------|--------------|
| Descoberta | 1 semana | 20h | Análise de requisitos, ERD |
| Extração | 2 semanas | 40h | Scripts ETL, testes, documentação |
| Transformação | 2 semanas | 40h | Transformações, validações, testes |
| Armazenamento | 1 semana | 20h | Schema, índices, testes |
| Visualização | 2 semanas | 40h | Dashboards, testes, validação |
| Documentação | 1 semana | 20h | Docs, guides, portfolio setup |
| **TOTAL** | **9 semanas** | **180h** | **Projeto Completo** |

---

## 9. RISCOS E MITIGAÇÕES

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|--------|-----------|
| API indisponível | Média | Médio | Mock data, retry logic |
| Performance BD | Baixa | Alto | Índices, particionamento |
| Qualidade de dados | Alta | Médio | Validações, alertas |
| Mudanças de requisitos | Média | Baixo | Documentação clara |
| Ambiente inconsistente | Média | Médio | Docker, requirements.txt |

---

## 10. CRITÉRIOS DE ACEITAÇÃO

- [ ] Extração de 100% dos endpoints funcionando
- [ ] Zero erro crítico em transformações
- [ ] 95% de dados validados com sucesso
- [ ] Dashboard com latência < 5 segundos
- [ ] Documentação 100% completa
- [ ] Cobertura de testes >= 80%
- [ ] Pipeline executado com sucesso (ponta a ponta)
- [ ] Código review aprovado (sem warnings)

---

## 11. PRÓXIMOS PASSOS

1. **Semana 1:**
   - [ ] Setup do ambiente (Python, PostgreSQL)
   - [ ] Criar repositório Git
   - [ ] Estruturar diretórios do projeto
   - [ ] Análise detalhada da API

2. **Semana 2-3:**
   - [ ] Implementar extractor
   - [ ] Criar testes
   - [ ] Setup do PostgreSQL

3. **Semana 4-5:**
   - [ ] Transformações e validações
   - [ ] Carga no warehouse

4. **Semana 6-7:**
   - [ ] Dashboards no Power BI
   - [ ] Testes end-to-end

5. **Semana 8-9:**
   - [ ] Documentação final
   - [ ] Portfolio preparation

---

## 12. CONTATO E REFERÊNCIAS

- **Fake Store API:** https://fakestoreapi.com/docs
- **GitHub Repository:** https://github.com/keikaavousi/fake-store-api
- **Documentação Interna:** (será criada durante o projeto)

---

**Aprovado por:** Seu Nome  
**Data de Aprovação:** Maio 2026  
**Versão Atual:** 1.0
