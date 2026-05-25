# ✅ CHECKLIST EXECUTÁVEL DO PROJETO

---

## FASE 0: PRÉ-REQUISITOS (Antes de Começar)

### Instalações Necessárias
- [ ] Python 3.11+ instalado
- [ ] PostgreSQL 14+ instalado e rodando
- [ ] Git instalado
- [ ] Power BI Desktop instalado
- [ ] VSCode ou IDE de preferência
- [ ] Postman (opcional, para testar API)

### Setup Inicial
- [ ] Criar repositório no GitHub (public para portfolio)
- [ ] Clonar repositório localmente
- [ ] Criar branch `develop` como principal de trabalho
- [ ] Criar arquivo `.gitignore` (incluir venv/, .env, __pycache__/, *.db)
- [ ] Criar arquivo `README.md` inicial

---

## FASE 1: DESCOBERTA E PLANEJAMENTO (1 semana)

### Semana 1 - Setup do Ambiente

#### 1.1 - Estrutura de Diretórios
- [ ] Criar estrutura de diretórios conforme documento técnico
- [ ] Criar arquivo `requirements.txt` com dependências
- [ ] Criar arquivo `requirements-dev.txt` com dev dependencies
- [ ] Criar arquivo `.env.example`
- [ ] Criar `Makefile` com comandos úteis

#### 1.2 - Ambiente Python
```bash
# Comandos a executar:
- [ ] python -m venv venv
- [ ] source venv/bin/activate
- [ ] pip install -r requirements.txt
- [ ] pip install -r requirements-dev.txt
```

#### 1.3 - Configuração de Logging
- [ ] Criar arquivo `src/logger.py`
- [ ] Configurar logging centralizado
- [ ] Testar logging em arquivo e console
- [ ] Documentar estrutura de logs

#### 1.4 - Exploração da API
- [ ] Acessar https://fakestoreapi.com/docs
- [ ] Testar cada endpoint com curl/Postman
- [ ] Documentar estrutura de resposta em JSON
- [ ] Identificar campos, tipos e possíveis nulos
- [ ] Criar notebook exploratório: `01_exploracao_api.ipynb`

#### 1.5 - Documentação Inicial
- [ ] Criar `docs/ARQUITETURA.md` com diagrama
- [ ] Criar `docs/API_MAPPING.md` mapeando endpoints
- [ ] Criar `docs/DICIONARIO_DADOS.md` (inicial)
- [ ] Documentar schema ERD esperado

#### 1.6 - Versionamento
- [ ] Fazer commit inicial: "Initial project setup"
- [ ] Criar tag v0.1.0
- [ ] Revisar .gitignore
- [ ] Fazer push para repositório

---

## FASE 2: EXTRAÇÃO DE DADOS (2 semanas)

### Semana 2 - Implementação do Extrator

#### 2.1 - Classes Base
- [ ] Criar `src/extractors/base_extractor.py` (classe abstrata)
- [ ] Definir interface padrão
- [ ] Implementar tratamento genérico de erros
- [ ] Criar exceções customizadas: `src/utils/exceptions.py`

#### 2.2 - Cliente HTTP
- [ ] Criar `src/extractors/api_client.py`
- [ ] Implementar session com retry logic
- [ ] Adicionar tratamento de timeout
- [ ] Testar conectividade com API

#### 2.3 - Extrator Principal
- [ ] Criar `src/extractors/fake_store_extractor.py`
- [ ] Implementar `extract_products()`
- [ ] Implementar `extract_categories()`
- [ ] Implementar `extract_users()`
- [ ] Implementar `extract_carts()`
- [ ] Implementar `extract_all()`
- [ ] Adicionar logging em cada método

#### 2.4 - Testes Unitários
- [ ] Criar `tests/test_extractors.py`
- [ ] Testar cada método com mocks
- [ ] Testar tratamento de erros
- [ ] Testar retry logic
- [ ] Atingir 80%+ cobertura

#### 2.5 - Integração Inicial
- [ ] Criar script `scripts/test_extraction.py`
- [ ] Executar extração real da API
- [ ] Validar dados recebidos
- [ ] Armazenar amostra em JSON para futuro

#### 2.6 - Commit
- [ ] Commit: "Implement data extraction layer"
- [ ] Tag: v0.2.0
- [ ] Push para develop

### Semana 3 - Refinamentos de Extração

#### 3.1 - Validações
- [ ] Adicionar validação de schema com Pydantic
- [ ] Validar tipos de dados
- [ ] Detectar valores nulos inesperados
- [ ] Registrar rejeições

#### 3.2 - Error Handling
- [ ] Implementar retry com backoff exponencial
- [ ] Adicionar circuit breaker
- [ ] Logging detalhado de erros
- [ ] Criação de relatório de erros

#### 3.3 - Performance
- [ ] Implementar request batching (se aplicável)
- [ ] Adicionar caching local
- [ ] Testar com dados grandes
- [ ] Documentar tempos de execução

#### 3.4 - Testes Integrados
- [ ] Testar fluxo completo de extração
- [ ] Validar volume de dados
- [ ] Testar com falhas simuladas
- [ ] Documentar tempo de execução

#### 3.5 - Documentação
- [ ] Atualizar `docs/API_MAPPING.md`
- [ ] Criar guia de troubleshooting
- [ ] Documentar padrões de erro conhecidos
- [ ] Criar exemplos de uso

#### 3.6 - Commit
- [ ] Commit: "Add validation and error handling"
- [ ] Tag: v0.3.0
- [ ] Push para develop

---

## FASE 3: TRANSFORMAÇÃO E LIMPEZA (2 semanas)

### Semana 4 - Data Cleaning

#### 4.1 - Implementação Base
- [ ] Criar `src/transformers/base_transformer.py`
- [ ] Criar `src/transformers/data_cleaner.py`
- [ ] Implementar `clean_products()`
- [ ] Implementar `clean_users()`
- [ ] Implementar `clean_carts()`
- [ ] Adicionar renomeação de colunas

#### 4.2 - Limpeza Detalhada
- [ ] Conversão de tipos de dados
- [ ] Tratamento de valores nulos
- [ ] Remoção de duplicatas
- [ ] Limpeza de espaços em branco
- [ ] Normalização de texto

#### 4.3 - Enriquecimento
- [ ] Criar `src/transformers/data_enricher.py`
- [ ] Adicionar timestamps de processamento
- [ ] Calcular agregações simples
- [ ] Criar flags de qualidade

#### 4.4 - Testes
- [ ] Criar `tests/test_transformers.py`
- [ ] Testar cada transformação
- [ ] Validar saída esperada
- [ ] Testar edge cases

#### 4.5 - Documentação
- [ ] Documentar regras de limpeza
- [ ] Criar exemplos antes/depois
- [ ] Listar decisões de design

#### 4.6 - Commit
- [ ] Commit: "Implement data cleaning and enrichment"
- [ ] Tag: v0.4.0

### Semana 5 - Validação e Quality

#### 5.1 - Validações
- [ ] Criar `src/transformers/validators.py`
- [ ] Validar ranges de valores (preços, quantidades)
- [ ] Validar padrões (email, telefone)
- [ ] Validar integridade referencial

#### 5.2 - Great Expectations
- [ ] Integrar Great Expectations
- [ ] Criar expectation suites
- [ ] Validar distribuição de dados
- [ ] Gerar data docs

#### 5.3 - Qualidade
- [ ] Implementar data quality checks
- [ ] Criar relatório de qualidade
- [ ] Definir SLAs de dados
- [ ] Alertas para anomalias

#### 5.4 - Pipeline ETL
- [ ] Criar `src/pipeline.py`
- [ ] Orquestrar extract → transform → validate
- [ ] Implementar error handling
- [ ] Logging de cada etapa
- [ ] Checkpoint de dados

#### 5.5 - Testes End-to-End
- [ ] Testar pipeline completo
- [ ] Validar dados transformados
- [ ] Testar recuperação de falhas
- [ ] Performance do pipeline

#### 5.6 - Commit
- [ ] Commit: "Add data validation and quality checks"
- [ ] Tag: v0.5.0

---

## FASE 4: ARMAZENAMENTO (1 semana)

### Semana 6 - Setup PostgreSQL

#### 6.1 - Banco de Dados
- [ ] PostgreSQL instalado e rodando
- [ ] Criar usuário de serviço: `sales_admin`
- [ ] Criar database: `sales_db`
- [ ] Configurar permissões

#### 6.2 - Schema (Staging)
- [ ] Criar schema `staging`
- [ ] Executar `stg_products`
- [ ] Executar `stg_users`
- [ ] Executar `stg_carts`
- [ ] Executar `stg_cart_items`
- [ ] Criar índices básicos

#### 6.3 - Schema (Warehouse)
- [ ] Criar schema `warehouse`
- [ ] Executar `dim_date` (popular com datas)
- [ ] Executar `dim_categories`
- [ ] Executar `dim_products`
- [ ] Executar `dim_users`
- [ ] Executar `fct_sales`
- [ ] Executar índices

#### 6.4 - ORM e Modelos
- [ ] Configurar SQLAlchemy
- [ ] Criar `src/models/staging.py`
- [ ] Criar `src/models/warehouse.py`
- [ ] Definir relacionamentos
- [ ] Testes de modelos

#### 6.5 - Loader
- [ ] Criar `src/loaders/database.py`
- [ ] Criar `src/loaders/postgres_loader.py`
- [ ] Implementar `load_dataframe()`
- [ ] Implementar `execute_sql()`
- [ ] Tratamento de transações
- [ ] Rollback em caso de erro

#### 6.6 - Testes
- [ ] Criar `tests/test_loaders.py`
- [ ] Testar conexão
- [ ] Testar carregamento de dados
- [ ] Testar integridade referencial
- [ ] Testar rollback

#### 6.7 - Migrations
- [ ] Criar `scripts/init_database.py`
- [ ] Script executa todos os schemas
- [ ] População de dim_date
- [ ] Versionamento de migrations

#### 6.8 - Commit
- [ ] Commit: "Implement PostgreSQL loader"
- [ ] Tag: v0.6.0

---

## FASE 5: VISUALIZAÇÃO (2 semanas)

### Semana 7 - Preparação de Dados

#### 7.1 - Views SQL
- [ ] Criar `v_sales_summary`
- [ ] Criar `v_monthly_sales`
- [ ] Criar `v_customer_analysis`
- [ ] Testar cada view
- [ ] Documentar

#### 7.2 - Agregações
- [ ] Criar tabelas de agregação (se necessário)
- [ ] Implementar refresh automático
- [ ] Indexação otimizada
- [ ] Testes de performance

#### 7.3 - Integração com Power BI
- [ ] Instalar driver ODBC PostgreSQL
- [ ] Teste de conexão
- [ ] Importar tabelas no Power BI
- [ ] Validar dados carregados

#### 7.4 - Preparação BI
- [ ] Criar modelo semântico
- [ ] Definir medidas DAX
- [ ] Criar tabelas de calendário
- [ ] Configurar relacionamentos

#### 7.5 - Commit
- [ ] Commit: "Add database views and aggregations"
- [ ] Tag: v0.7.0

### Semana 8 - Dashboards Power BI

#### 8.1 - Dashboard Executivo
- [ ] Criar página: "Overview"
- [ ] KPI Cards: Revenue, Transactions, Avg Ticket
- [ ] Gráfico de tendência: Last 12 months
- [ ] Top 10 Products
- [ ] Sales by Category
- [ ] Validar números

#### 8.2 - Dashboard Detalhado
- [ ] Criar página: "Analysis"
- [ ] Heat map: Vendas por período
- [ ] Bar chart: Por categoria
- [ ] Tabela: Top customers
- [ ] Histograma: Distribuição de tickets
- [ ] Filtros interativos

#### 8.3 - Dashboard Analítico
- [ ] Criar página: "Insights"
- [ ] Correlation analysis
- [ ] Customer segmentation
- [ ] Seasonality analysis
- [ ] Trend forecasting (se possível)
- [ ] Drill-down capabilities

#### 8.4 - Formatação e UX
- [ ] Aplicar tema corporativo
- [ ] Verificar acessibilidade
- [ ] Otimizar cores e fontes
- [ ] Testar performance
- [ ] Adicionar tooltips informativos

#### 8.5 - Testes
- [ ] Verificar fórmulas DAX
- [ ] Validar cálculos
- [ ] Testar filtros
- [ ] Cross-page navigation
- [ ] Performance (< 5s por interação)

#### 8.6 - Documentação
- [ ] Criar `dashboards/README.md`
- [ ] Explicar cada visual
- [ ] Glossário de termos
- [ ] Guia de uso para stakeholders

#### 8.7 - Commit
- [ ] Commit: "Create executive dashboards in Power BI"
- [ ] Tag: v0.8.0

---

## FASE 6: AUTOMAÇÃO E DOCUMENTAÇÃO (1 semana)

### Semana 9 - Automação e Finalização

#### 9.1 - Scheduler
- [ ] Criar `src/scheduler.py`
- [ ] Configurar APScheduler
- [ ] Agendar extração (ex: diariamente 02:00)
- [ ] Implementar notificações de erro
- [ ] Logging de execução

#### 9.2 - Scripts de Utilitário
- [ ] Criar `scripts/run_pipeline.py` (manual)
- [ ] Criar `scripts/backup_restore.py`
- [ ] Criar `scripts/health_check.py`
- [ ] Criar `scripts/cleanup.py`

#### 9.3 - Docker (Opcional mas Recomendado)
- [ ] Criar `Dockerfile` para aplicação
- [ ] Criar `docker-compose.yml`
- [ ] Incluir PostgreSQL
- [ ] Documentar container setup
- [ ] Testar execução em container

#### 9.4 - CI/CD (GitHub Actions)
- [ ] Criar `.github/workflows/tests.yml`
- [ ] Criar `.github/workflows/lint.yml`
- [ ] Executar testes em push
- [ ] Executar linting automático
- [ ] Badge no README

#### 9.5 - Documentação Completa
- [ ] `README.md` completo (com badges)
- [ ] `INSTALLATION.md` - Como instalar
- [ ] `USAGE.md` - Como usar
- [ ] `TROUBLESHOOTING.md` - Problemas comuns
- [ ] `CONTRIBUTING.md` - Como contribuir
- [ ] `LICENSE` - Licença (MIT recomendado)

#### 9.6 - Dicionário de Dados
- [ ] Documentar cada tabela
- [ ] Documentar cada coluna
- [ ] Incluir exemplos de valores
- [ ] Incluir relacionamentos
- [ ] Dicionário em Excel/PDF

#### 9.7 - Apresentação do Projeto
- [ ] Criar `PORTFOLIO.md` explicando o projeto
- [ ] Incluir screenshots dos dashboards
- [ ] Descrever stack técnico
- [ ] Listar aprendizados
- [ ] Explicar desafios enfrentados

#### 9.8 - Code Quality Final
- [ ] Executar `black` para formatação
- [ ] Executar `isort` para imports
- [ ] Executar `flake8` para linting
- [ ] Executar `mypy` para type checking
- [ ] Corrigir todos os warnings

#### 9.9 - Testes Finais
- [ ] Executar `pytest` com cobertura
- [ ] Verificar cobertura >= 80%
- [ ] Testar pipeline completo
- [ ] Validar dados em Power BI
- [ ] Documentar resultados

#### 9.10 - Limpeza Final
- [ ] Remover código comentado
- [ ] Remover imports não utilizados
- [ ] Remover prints de debug
- [ ] Verificar credenciais (nunca em código)
- [ ] Último review do código

#### 9.11 - Commit e Release
- [ ] Commit: "Final documentation and cleanup"
- [ ] Merge `develop` → `main`
- [ ] Tag: v1.0.0
- [ ] Release notes no GitHub
- [ ] Push para production

#### 9.12 - Portfolio
- [ ] Adicionar projeto ao GitHub
- [ ] Adicionar ao LinkedIn
- [ ] Criar pequeno write-up no Medium/Dev.to
- [ ] Compartilhar no Twitter/comunidades
- [ ] Pedir feedback

---

## CHECKLIST FINAL - VALIDAÇÕES

### Código
- [ ] 100% das funções têm docstrings
- [ ] 100% das funções têm type hints
- [ ] Nenhum warning do mypy
- [ ] Cobertura >= 80%
- [ ] Sem hardcoded credentials
- [ ] Sem TODO's pendentes

### Documentação
- [ ] README completo e claro
- [ ] Guia de instalação funcionando
- [ ] Dicionário de dados atualizado
- [ ] Exemplos de execução
- [ ] Screenshots dos dashboards
- [ ] Changelog atualizado

### Dados
- [ ] Pipeline executa sem erros
- [ ] 100% dos dados validados
- [ ] Zero dados duplicados indevidos
- [ ] Integridade referencial OK
- [ ] Logs claros e informativos

### Dashboard
- [ ] Todos os KPIs corretos
- [ ] Filtros funcionam
- [ ] Performance < 5 segundos
- [ ] Sem erros de cálculo
- [ ] Visualmente atraente

### Deploy
- [ ] Pronto para executar em outro PC
- [ ] Instruções claras de setup
- [ ] Backup automático configurado
- [ ] Monitoramento implementado
- [ ] Plano de manutenção documentado

---

## PONTOS FINAIS IMPORTANTES

✅ **Faça commits frequentes** (pelo menos 1 por dia)  
✅ **Teste constantemente** (não deixe para o final)  
✅ **Documente enquanto desenvolve** (não é tarefa final)  
✅ **Peça feedback** durante o desenvolvimento  
✅ **Revise e refatore** regularmente  
✅ **Mantenha histórico limpo** com boas mensagens de commit  
✅ **Preserve dados de test** para reprodução  

---

**Tempo Total Estimado:** 8-10 semanas  
**Horas de Dedicação:** ~180 horas  
**Intensidade:** ~20-25h por semana (trabalho em tempo parcial)

Boa sorte! 🚀
