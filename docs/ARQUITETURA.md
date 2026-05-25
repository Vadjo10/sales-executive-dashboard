# Architecture

```
┌──────────────────────────────────────┐
│         FAKE STORE API               │
│  (Products, Carts, Users, Categories)│
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│     EXTRACTION LAYER (Python)        │
│  • APIClient (httpx + retry)         │
│  • FakeStoreExtractor                │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│   TRANSFORMATION LAYER (Pandas)      │
│  • DataCleaner                       │
│  • DataEnricher                      │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│     STORAGE LAYER (PostgreSQL)       │
│  • staging schema (raw data)         │
│  • warehouse schema (star schema)    │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│   VISUALIZATION LAYER (Power BI)     │
│  • Executive Dashboard               │
│  • Sales KPIs                        │
│  • Interactive Reports               │
└──────────────────────────────────────┘
```

## Layers

### Extraction
- **APIClient**: HTTP client with automatic retry and timeout
- **FakeStoreExtractor**: Entity-specific extraction methods

### Transformation
- **DataCleaner**: Removes duplicates, converts types, cleans strings
- **DataEnricher**: Adds processing metadata

### Storage
- **Staging**: Raw data mirror of API responses
- **Warehouse**: Star schema with dimensions and facts

### Visualization
- Power BI dashboards connecting directly to PostgreSQL
