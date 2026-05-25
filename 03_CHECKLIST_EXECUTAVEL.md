# ✅ CHECKLIST EXECUTÁVEL DO PROJETO

---

## FASE 0: PRÉ-REQUISITOS (Antes de Começar)

### Instalações Necessárias
- [x] Python 3.11+ instalado
- [x] PostgreSQL 14+ instalado e rodando
- [x] Git instalado
- [ ] Power BI Desktop instalado
- [ ] VSCode ou IDE de preferência
- [ ] Postman (opcional, para testar API)

### Setup Inicial
- [x] Criar repositório no GitHub (public para portfolio)
- [x] Clonar repositório localmente
- [ ] Criar branch `develop` como principal de trabalho
- [x] Criar arquivo `.gitignore` (incluir venv/, .env, __pycache__/, *.db)
- [x] Criar arquivo `README.md` inicial

---

## FASE 1: DESCOBERTA E PLANEJAMENTO (1 semana)

### Semana 1 - Setup do Ambiente

#### 1.1 - Estrutura de Diretórios
- [x] Criar estrutura de diretórios conforme documento técnico
- [x] Criar arquivo `requirements.txt` com dependências
- [x] Criar arquivo `requirements-dev.txt` com dev dependencies
- [x] Criar arquivo `.env.example`
- [x] Criar `Makefile` com comandos úteis

#### 1.2 - Ambiente Python
```bash
# Comandos a executar:
- [x] python -m venv venv
- [x] source venv/bin/activate
- [x] pip install -r requirements.txt
- [x] pip install -r requirements-dev.txt
```

#### 1.3 - Configuração de Logging
- [x] Criar arquivo `src/logger.py`
- [x] Configurar logging centralizado
- [x] Testar logging em arquivo e console
- [x] Documentar estrutura de logs

#### 1.4 - Exploração da API
- [x] Acessar https://fakestoreapi.com/docs
- [x] Testar cada endpoint com curl/Postman
- [x] Documentar estrutura de resposta em JSON
- [x] Identificar campos, tipos e possíveis nulos
- [ ] Criar notebook exploratório: `01_exploracao_api.ipynb`

#### 1.5 - Documentação Inicial
- [x] Criar `docs/ARQUITETURA.md` com diagrama
- [x] Criar `docs/API_MAPPING.md` mapeando endpoints
- [ ] Criar `docs/DICIONARIO_DADOS.md` (inicial)
- [ ] Documentar schema ERD esperado

#### 1.6 - Versionamento
- [x] Fazer commit inicial: "Initial project setup"
- [ ] Criar tag v0.1.0
- [x] Revisar .gitignore
- [x] Fazer push para repositório

---

## FASE 2: EXTRAÇÃO DE DADOS (2 semanas)

### Semana 2 - Implementação do Extrator

#### 2.1 - Classes Base
- [x] Criar `src/extractors/base_extractor.py` (classe abstrata)
- [x] Definir interface padrão
- [x] Implementar tratamento genérico de erros
- [x] Criar exceções customizadas: `src/utils/exceptions.py`

#### 2.2 - Cliente HTTP
- [x] Criar `src/extractors/api_client.py`
- [x] Implementar session com retry logic
- [x] Adicionar tratamento de timeout
- [x] Testar conectividade com API

#### 2.3 - Extrator Principal
- [x] Criar `src/extractors/fake_store_extractor.py`
- [x] Implementar `extract_products()`
- [x] Implementar `extract_categories()`
- [x] Implementar `extract_users()`
- [x] Implementar `extract_carts()`
- [x] Implementar `extract_all()`
- [x] Adicionar logging em cada método

#### 2.4 - Testes Unitários
- [x] Criar `tests/test_extractors.py`
- [x] Testar cada método com mocks
- [x] Testar tratamento de erros
- [x] Testar retry logic
- [ ] Atingir 80%+ cobertura

#### 2.5 - Integração Inicial
- [x] Criar script `scripts/test_api_data.py`
- [x] Executar extração real da API
- [x] Validar dados recebidos
- [x] Armazenar amostra em JSON para futuro

#### 2.6 - Commit
- [x] Commit: "Implement data extraction layer"
- [ ] Tag: v0.2.0
- [x] Push para repositório

### Semana 3 - Refinamentos de Extração

#### 3.1 - Validações
- [ ] Adicionar validação de schema com Pydantic
- [x] Validar tipos de dados
- [x] Detectar valores nulos inesperados
- [ ] Registrar rejeições

#### 3.2 - Error Handling
- [x] Implementar retry com backoff exponencial
- [ ] Adicionar circuit breaker
- [x] Logging detalhado de erros
- [ ] Criação de relatório de erros

#### 3.3 - Performance
- [ ] Implementar request batching (se aplicável)
- [ ] Adicionar caching local
- [ ] Testar com dados grandes
- [ ] Documentar tempos de execução

#### 3.4 - Testes Integrados
- [x] Testar fluxo completo de extração
- [x] Validar volume de dados
- [ ] Testar com falhas simuladas
- [ ] Documentar tempo de execução

#### 3.6 - Commit
- [ ] Commit: "Add validation and error handling"
- [ ] Tag: v0.3.0
- [ ] Push para develop

---

## FASE 3: TRANSFORMAÇÃO E LIMPEZA (2 semanas)

### Semana 4 - Data Cleaning

#### 4.1 - Implementação Base
- [x] Criar `src/transformers/base_transformer.py`
- [x] Criar `src/transformers/data_cleaner.py`
- [x] Implementar `clean_products()` (genérico)
- [x] Implementar `clean_users()` (genérico)
- [x] Implementar `clean_carts()` (genérico)
- [x] Adicionar renomeação de colunas

#### 4.2 - Limpeza Detalhada
- [x] Conversão de tipos de dados
- [x] Tratamento de valores nulos
- [x] Remoção de duplicatas
- [x] Limpeza de espaços em branco
- [x] Normalização de texto

#### 4.3 - Enriquecimento
- [x] Criar `src/transformers/data_enricher.py`
- [x] Adicionar timestamps de processamento
- [ ] Calcular agregações simples
- [ ] Criar flags de qualidade

#### 4.4 - Testes
- [x] Criar `tests/test_transformers.py`
- [x] Testar cada transformação
- [x] Validar saída esperada
- [x] Testar edge cases

### Semana 5 - Validação e Quality

#### 5.1 - Validações
- [x] Criar `src/utils/validators.py`
- [x] Validar ranges de valores (preços, quantidades)
- [x] Validar padrões (email, telefone)
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
- [x] Criar `src/pipeline.py`
- [x] Orquestrar extract → transform → load
- [x] Implementar error handling
- [x] Logging de cada etapa
- [ ] Checkpoint de dados

#### 5.5 - Testes End-to-End
- [x] Testar pipeline completo
- [x] Validar dados transformados
- [ ] Testar recuperação de falhas
- [x] Performance do pipeline

---

## FASE 4: ARMAZENAMENTO (1 semana)

### Semana 6 - Setup PostgreSQL

#### 6.1 - Banco de Dados
- [x] PostgreSQL instalado e rodando (Docker)
- [x] Criar usuário de serviço: `dsa`
- [x] Criar database: `sales_db`
- [ ] Configurar permissões

#### 6.2 - Schema (Staging)
- [x] Criar schema `staging`
- [x] Executar `stg_products`
- [x] Executar `stg_users`
- [x] Executar `stg_carts`
- [x] Executar `stg_categories`
- [ ] Executar `stg_cart_items`
- [ ] Criar índices básicos

#### 6.3 - Schema (Warehouse)
- [x] Criar schema `warehouse`
- [x] Executar `dim_date` (popular com datas)
- [x] Executar `dim_categories`
- [x] Executar `dim_products`
- [x] Executar `dim_users`
- [x] Executar `fct_sales`
- [ ] Executar índices

#### 6.4 - ORM e Modelos
- [x] Configurar SQLAlchemy
- [x] Criar `src/models/staging.py`
- [x] Criar `src/models/warehouse.py`
- [x] Definir relacionamentos
- [ ] Testes de modelos

#### 6.5 - Loader
- [x] Criar `src/loaders/database.py`
- [x] Criar `src/loaders/postgres_loader.py`
- [x] Implementar `load_dataframe()`
- [x] Implementar `execute_sql()`
- [ ] Tratamento de transações
- [ ] Rollback em caso de erro

#### 6.6 - Testes
- [x] Criar `tests/test_loaders.py`
- [x] Testar conexão
- [x] Testar carregamento de dados
- [ ] Testar integridade referencial
- [ ] Testar rollback

#### 6.7 - Migrations
- [x] Criar `scripts/init_database.py`
- [x] Script executa todos os schemas
- [x] População de dim_date
- [ ] Versionamento de migrations

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
- [x] Criar `scripts/scheduler.py`
- [x] Configurar APScheduler
- [x] Agendar extração (ex: diariamente 02:00)
- [ ] Implementar notificações de erro
- [x] Logging de execução

#### 9.2 - Scripts de Utilitário
- [x] Criar `scripts/run_pipeline.py` (manual)
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
- [x] 100% das funções têm type hints
- [ ] Nenhum warning do mypy
- [ ] Cobertura >= 80%
- [x] Sem hardcoded credentials (usamos .env)
- [ ] Sem TODO's pendentes

### Documentação
- [ ] README completo e claro
- [ ] Guia de instalação funcionando
- [ ] Dicionário de dados atualizado
- [ ] Exemplos de execução
- [ ] Screenshots dos dashboards
- [ ] Changelog atualizado

### Dados
- [x] Pipeline executa sem erros
- [x] 100% dos dados validados (test_api_data.py)
- [ ] Zero dados duplicados indevidos
- [ ] Integridade referencial OK
- [x] Logs claros e informativos

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
