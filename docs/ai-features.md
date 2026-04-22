# ActuFlow AI Features

## Overview

ActuFlow includes optional AI-powered features that augment user workflows without replacing auditable, deterministic calculations. All AI features can be disabled individually or entirely.

## Design Principles

1. **AI Assists, Never Decides**: AI suggestions always require human confirmation
2. **Graceful Degradation**: All features work without AI enabled
3. **Transparency**: AI outputs are clearly marked and explainable
4. **Auditability**: All AI interactions are logged
5. **Privacy First**: Sensitive data handling follows strict rules

## Feature Catalog

### 1. Smart Data Import

**What it does:**
- Auto-detects column mappings when uploading CSV/Excel files
- Identifies data quality issues (missing values, outliers, format mismatches)
- Suggests corrections for common errors

**How it works:**
```
1. User uploads file
2. System extracts column names and sample values
3. AI analyzes headers against known field names
4. Pattern matching identifies data types and formats
5. Returns confidence scores for each suggested mapping
6. User reviews and confirms/modifies mappings
```

**Example output:**
```json
{
  "suggestions": [
    {
      "source_column": "DOB",
      "target_field": "date_of_birth",
      "confidence": 0.95,
      "reason": "Column name matches common abbreviation for date of birth"
    },
    {
      "source_column": "Sum Ins",
      "target_field": "sum_assured",
      "confidence": 0.82,
      "reason": "Values are large currency amounts, header suggests sum insured"
    }
  ],
  "data_issues": [
    {
      "column": "premium",
      "issue": "negative_values",
      "count": 3,
      "rows": [145, 892, 1203],
      "suggestion": "Negative premiums may indicate refunds or errors"
    }
  ]
}
```

**Feature flag:** `AI_SMART_IMPORT`

### 2. Natural Language Query Interface

**What it does:**
- Accepts questions in plain English
- Generates filters, reports, and navigates to records
- Works across policies, claims, calculations, reports

**How it works:**
```
1. User types natural language query
2. NLP model parses intent and entities
3. System validates query against user's permissions
4. Generates structured API query
5. Executes query and formats results
6. Returns answer with explanation of interpretation
```

**Example queries:**
- "Show me all lapsed policies from Q1 2024"
- "Which products had the highest claim ratio last year?"
- "Find policies with sum assured over $1M issued to smokers"
- "Compare reserves between December and March runs"

**Security:** Queries are translated to API calls, never to raw SQL. User permissions are always enforced.

**Feature flag:** `AI_NATURAL_LANGUAGE`

### 3. Anomaly Detection

**What it does:**
- Flags calculation results that deviate from historical norms
- Identifies potentially suspicious claims patterns
- Detects data entry errors in real-time

**How it works:**
- Statistical models (Isolation Forest) trained on historical data
- Rules-based checks for known patterns
- Comparison against portfolio benchmarks

**Anomaly types:**
- **Calculation anomalies**: Reserve values outside expected range
- **Claims anomalies**: Unusual claim patterns or amounts
- **Data anomalies**: Values that don't match expected distributions

**Important:** All anomalies are flagged for human review. No automatic actions are taken.

**Feature flag:** `AI_ANOMALY_DETECTION`

### 4. Narrative Generation

**What it does:**
- Auto-generates executive summaries for calculation runs
- Creates plain-English explanations of reserve movements
- Drafts variance commentary for board reports

**Example output:**
```
Reserve Movement Summary - Q4 2024

Total reserves increased by $12.3M (4.2%) from the prior quarter.

Key drivers:
• New business added $8.1M in reserves (156 new policies)
• Assumption update reduced reserves by $2.4M (mortality improvement)
• Experience variance added $6.6M (higher than expected claims)

Notable items requiring attention:
• Term life segment shows 15% higher claims than expected
• Three policies flagged for reserve anomalies (see detailed report)
```

**User workflow:** AI generates draft → User reviews and edits → Final version saved

**Feature flag:** `AI_NARRATIVE_GENERATION`

### 5. Semantic Search

**What it does:**
- Search by meaning, not just keywords
- Find similar policies or claims
- Search across documents and notes

**How it works:**
- Text is converted to vector embeddings
- Similarity search using pgvector
- Results ranked by relevance score

**Use cases:**
- "Find policies similar to POL-2024-12345"
- Search for documents mentioning "rate increase rationale"
- Find claims with similar circumstances

**Feature flag:** `AI_SEMANTIC_SEARCH`

### 6. Document Extraction

**What it does:**
- Extracts text from scanned documents (OCR)
- Identifies structured data (names, dates, amounts)
- Auto-populates forms from uploaded applications

**Supported document types:**
- Policy applications
- Claim forms
- Medical reports
- Identification documents

**Extraction workflow:**
```
1. User uploads document
2. OCR extracts raw text
3. AI identifies entities (names, dates, amounts, policy numbers)
4. Confidence scores assigned to each extraction
5. User reviews and corrects extractions
6. Confirmed data can be used to create/update records
```

**Feature flag:** `AI_DOCUMENT_EXTRACTION`

### 7. Experience Recommendations

**What it does:**
- Compares assumed rates to actual experience
- Suggests assumption updates based on credible data
- Highlights segments where assumptions are most off

**Output example:**
```json
{
  "recommendations": [
    {
      "assumption_type": "mortality",
      "segment": "male_smoker_45-54",
      "current_rate": 0.0045,
      "actual_rate": 0.0052,
      "credibility": 0.78,
      "suggested_rate": 0.0050,
      "impact": {
        "reserve_change": 2340000,
        "direction": "increase"
      },
      "confidence": "high",
      "data_points": 1247
    }
  ]
}
```

**Feature flag:** `AI_EXPERIENCE_RECOMMENDATIONS`

## Configuration

### Enabling/Disabling AI

**Master switch:**
```
AI_ENABLED=false  # Disables ALL AI features
```

**Individual features:**
```
AI_SMART_IMPORT=true
AI_NATURAL_LANGUAGE=false
AI_ANOMALY_DETECTION=true
...
```

### LLM Provider Configuration

**OpenAI (default):**
```
OPENAI_API_KEY=sk-xxx
OPENAI_MODEL=gpt-4-turbo-preview
```

**Azure OpenAI (enterprise):**
```
AZURE_OPENAI_ENDPOINT=https://xxx.openai.azure.com/
AZURE_OPENAI_API_KEY=xxx
AZURE_OPENAI_DEPLOYMENT=gpt-4
```

**Self-hosted (Ollama):**
```
OLLAMA_URL=http://ollama:11434
OLLAMA_MODEL=llama2
```

## Privacy & Compliance

### Data Handling

- **PII Minimization**: Only necessary data sent to AI services
- **Data Residency**: Azure OpenAI option for data residency requirements
- **Self-hosted Option**: Ollama for complete on-premise deployment

### Audit Trail

All AI interactions are logged:
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "user_id": "uuid",
  "feature": "natural_language_query",
  "input": "Show me lapsed policies",
  "output": {"filter": {"status": "lapsed"}, "count": 234},
  "latency_ms": 450
}
```

### User Controls

Users can configure AI preferences:
- Disable AI features for their account
- Opt out of query history storage
- Control narrative generation defaults

## Performance

### Latency Targets

| Feature | Target | P99 |
|---------|--------|-----|
| Column mapping | < 2s | 5s |
| NL query parsing | < 1s | 3s |
| Embedding generation | < 500ms | 1s |
| Document extraction | < 30s | 60s |
| Narrative generation | < 5s | 15s |

### Scaling

- AI service can be scaled independently
- Caching for repeated queries
- Batch processing for large imports
