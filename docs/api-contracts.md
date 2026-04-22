# ActuFlow API Contracts

## Overview

This document defines the API contract between the frontend and backend. All endpoints are prefixed with `/api/v1`.

## Authentication

### POST /auth/login

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### POST /auth/refresh

**Request:**
```json
{
  "refresh_token": "eyJ..."
}
```

### GET /auth/me

**Response:**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "John Smith",
  "role": {
    "id": "uuid",
    "name": "actuary",
    "permissions": ["policy:read", "calculation:create"]
  },
  "department": "Actuarial"
}
```

---

## Common Patterns

### Pagination

All list endpoints support pagination:

```
GET /policies?page=1&page_size=20
```

**Response:**
```json
{
  "items": [...],
  "total": 1234,
  "page": 1,
  "page_size": 20,
  "pages": 62
}
```

### Filtering

Filter using query parameters:

```
GET /policies?status=active&product_type=term_life
```

### Sorting

```
GET /policies?sort_by=created_at&sort_order=desc
```

### Error Response

```json
{
  "detail": "Policy not found",
  "code": "NOT_FOUND",
  "field": null
}
```

---

## Policies

### GET /policies

**Query Parameters:**
- `page`, `page_size`: Pagination
- `status`: active, lapsed, surrendered, matured, claimed
- `product_type`: term_life, whole_life, universal_life, etc.
- `product_code`: Product code filter
- `policyholder_id`: Filter by policyholder
- `issue_date_from`, `issue_date_to`: Date range
- `search`: Search policy number, holder name

### GET /policies/{id}

**Response:**
```json
{
  "id": "uuid",
  "policy_number": "POL-2024-000001",
  "product_type": "term_life",
  "product_code": "TERM-20",
  "product_name": "20-Year Term Life",
  "status": "active",
  "policyholder": {
    "id": "uuid",
    "full_name": "John Smith",
    "date_of_birth": "1980-05-15"
  },
  "issue_date": "2024-01-15",
  "effective_date": "2024-01-15",
  "maturity_date": "2044-01-15",
  "sum_assured": 500000.00,
  "premium_amount": 1200.00,
  "premium_frequency": "annual",
  "currency": "USD",
  "coverages": [...],
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### POST /policies

**Request:**
```json
{
  "policy_number": "POL-2024-000001",
  "product_type": "term_life",
  "product_code": "TERM-20",
  "policyholder_id": "uuid",
  "issue_date": "2024-01-15",
  "effective_date": "2024-01-15",
  "sum_assured": 500000.00,
  "premium_amount": 1200.00,
  "premium_frequency": "annual",
  "currency": "USD"
}
```

### PUT /policies/{id}

Same as POST, partial updates allowed.

### DELETE /policies/{id}

Soft delete. Returns 204 No Content.

---

## Assumptions

### GET /assumption-sets

**Query Parameters:**
- `status`: draft, pending_approval, approved, archived
- `search`: Search by name

### POST /assumption-sets/{id}/submit

Submit for approval. Changes status to `pending_approval`.

### POST /assumption-sets/{id}/approve

**Request:**
```json
{
  "approval_notes": "Approved after review"
}
```

### POST /assumption-sets/{id}/reject

**Request:**
```json
{
  "rejection_reason": "Mortality rates need revision"
}
```

### GET /assumption-sets/{id}/compare/{other_id}

**Response:**
```json
{
  "set_a": { "id": "uuid", "name": "2024 Q1", "version": "1.0" },
  "set_b": { "id": "uuid", "name": "2024 Q2", "version": "1.1" },
  "differences": [
    {
      "table_type": "mortality",
      "table_name": "Base Mortality",
      "changes": [
        {
          "key": "age_45_male",
          "value_a": 0.0025,
          "value_b": 0.0023,
          "change_percent": -8.0
        }
      ]
    }
  ]
}
```

---

## Calculations

### POST /calculations

**Request:**
```json
{
  "run_name": "Monthly Valuation - January 2024",
  "model_definition_id": "uuid",
  "assumption_set_id": "uuid",
  "policy_filter": {
    "status": "active",
    "product_type": ["term_life", "whole_life"]
  },
  "parameters": {
    "valuation_date": "2024-01-31",
    "reporting_basis": "IFRS17"
  }
}
```

**Response (202):**
```json
{
  "id": "uuid",
  "run_name": "Monthly Valuation - January 2024",
  "status": "queued",
  "created_at": "2024-02-01T10:30:00Z"
}
```

### GET /calculations/{id}/progress

**Response:**
```json
{
  "status": "running",
  "progress_percent": 45,
  "progress_message": "Processing batch 45 of 100",
  "policies_processed": 4500,
  "policies_total": 10000,
  "started_at": "2024-02-01T10:30:00Z",
  "estimated_completion": "2024-02-01T10:45:00Z"
}
```

### GET /calculations/{id}/results

**Query Parameters:**
- `policy_id`: Filter by policy
- `result_type`: reserve, cashflow, etc.
- `projection_month`: Specific month
- `anomaly_only`: Only return flagged results

### GET /calculations/{id}/narrative

**Response:**
```json
{
  "narrative": "Total reserves increased by $12.3M (4.2%)...",
  "generated_at": "2024-02-01T10:50:00Z",
  "key_points": [
    "New business added $8.1M in reserves",
    "Experience variance added $6.6M"
  ]
}
```

---

## AI Endpoints

### POST /ai/query

**Request:**
```json
{
  "query": "Show me all lapsed policies from Q1 with premium over $5000",
  "context": {
    "current_page": "policies"
  }
}
```

**Response:**
```json
{
  "query": "Show me all lapsed policies from Q1 with premium over $5000",
  "parsed_intent": {
    "intent": "search",
    "entity_type": "policy",
    "filters": {
      "status": "lapsed",
      "issue_date_from": "2024-01-01",
      "issue_date_to": "2024-03-31",
      "premium_amount_min": 5000
    }
  },
  "explanation": "Searching for policies with status 'lapsed', issued between Jan-Mar 2024, with premium amount greater than $5,000",
  "result_count": 45,
  "suggested_api_call": {
    "endpoint": "/api/v1/policies",
    "method": "GET",
    "params": {
      "status": "lapsed",
      "issue_date_from": "2024-01-01",
      "issue_date_to": "2024-03-31",
      "premium_min": 5000
    }
  }
}
```

### POST /ai/extract-document

**Request:** Multipart form with file upload

**Response:**
```json
{
  "document_id": "uuid",
  "extracted_text": "...",
  "entities": [
    {
      "type": "policy_number",
      "value": "POL-2024-000123",
      "confidence": 0.95
    },
    {
      "type": "date",
      "value": "2024-01-15",
      "confidence": 0.88
    },
    {
      "type": "amount",
      "value": 500000,
      "confidence": 0.92
    }
  ],
  "structured_data": {
    "policy_number": {"value": "POL-2024-000123", "confidence": 0.95},
    "sum_assured": {"value": 500000, "confidence": 0.92}
  }
}
```

---

## Automation

### GET /scheduled-jobs

### POST /scheduled-jobs

**Request:**
```json
{
  "name": "Monthly Reserve Calculation",
  "description": "Run reserve calculation on first of month",
  "job_type": "calculation",
  "cron_expression": "0 2 1 * *",
  "is_active": true,
  "config": {
    "model_definition_id": "uuid",
    "assumption_set_id": "uuid",
    "policy_filter": {"status": "active"}
  }
}
```

### POST /scheduled-jobs/{id}/run-now

Trigger immediate execution. Returns job execution ID.

### GET /scheduled-jobs/{id}/executions

**Response:**
```json
{
  "items": [
    {
      "id": "uuid",
      "started_at": "2024-02-01T02:00:00Z",
      "completed_at": "2024-02-01T02:15:23Z",
      "status": "completed",
      "result_summary": {
        "policies_processed": 15234,
        "duration_seconds": 923
      }
    }
  ]
}
```

### GET /automation-rules

### POST /automation-rules

**Request:**
```json
{
  "name": "High Value Claim Alert",
  "trigger_type": "claim_filed",
  "trigger_config": {
    "amount_threshold": 500000
  },
  "action_type": "send_notification",
  "action_config": {
    "user_ids": ["uuid"],
    "title": "High Value Claim Filed",
    "message": "A claim exceeding $500K has been filed."
  },
  "is_active": true
}
```

---

## WebSocket Endpoints

### /ws/calculations/{id}

Real-time calculation progress updates.

**Messages:**
```json
{"type": "progress", "data": {"percent": 45, "message": "..."}}
{"type": "completed", "data": {"summary": {...}}}
{"type": "failed", "data": {"error": "..."}}
```

### /ws/notifications

Real-time notifications for the authenticated user.

**Messages:**
```json
{"type": "notification", "data": {"id": "uuid", "title": "...", "message": "..."}}
```
