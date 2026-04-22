# ActuFlow Architecture

## Overview

ActuFlow is a microservices-based platform designed for insurance data management and actuarial calculations. The system is built for scalability, maintainability, and regulatory compliance.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                  CLIENTS                                     │
│                    (Web Browser, Mobile, API Consumers)                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              LOAD BALANCER                                   │
│                           (Nginx / Cloud LB)                                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    ▼                                   ▼
┌───────────────────────────────┐   ┌───────────────────────────────────────┐
│         FRONTEND              │   │              BACKEND API               │
│     (React + Nginx)           │   │           (FastAPI + Python)           │
│                               │   │                                       │
│  • Single Page Application    │   │  • RESTful API                        │
│  • TypeScript                 │   │  • WebSocket for real-time            │
│  • Ant Design UI              │   │  • JWT Authentication                 │
│  • TanStack Table/Query       │   │  • RBAC Authorization                 │
└───────────────────────────────┘   └───────────────────────────────────────┘
                                                      │
                    ┌─────────────────────────────────┼─────────────────────┐
                    │                                 │                     │
                    ▼                                 ▼                     ▼
┌─────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────┐
│   CALCULATION ENGINE    │  │      AI SERVICE             │  │    KEYCLOAK     │
│   (Celery Workers)      │  │   (FastAPI + ML Models)     │  │   (Identity)    │
│                         │  │                             │  │                 │
│ • Actuarial models      │  │ • NLP Query Processing      │  │ • SSO/OIDC      │
│ • NumPy/SciPy/Pandas    │  │ • Document Extraction       │  │ • LDAP/AD       │
│ • Async job processing  │  │ • Anomaly Detection         │  │ • User Mgmt     │
│ • Report generation     │  │ • Embeddings & Search       │  │                 │
└─────────────────────────┘  └─────────────────────────────┘  └─────────────────┘
          │                              │
          └──────────────┬───────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              MESSAGE BROKER                                  │
│                                 (Redis)                                      │
│                                                                             │
│  • Celery task queue       • Caching        • Session storage              │
│  • Pub/Sub for WebSocket   • Rate limiting  • Real-time updates            │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA LAYER                                      │
├──────────────────────┬───────────────────────┬──────────────────────────────┤
│     PostgreSQL       │    Elasticsearch      │         MinIO/S3             │
│                      │                       │                              │
│ • Primary database   │ • Full-text search    │ • File storage               │
│ • pgvector for       │ • Audit log indexing  │ • Report outputs             │
│   embeddings         │ • Policy search       │ • Document uploads           │
│ • JSONB for flex     │                       │ • Backups                    │
│   data               │                       │                              │
└──────────────────────┴───────────────────────┴──────────────────────────────┘
```

## Service Descriptions

### Frontend (React)
- **Purpose**: User interface for all ActuFlow functionality
- **Technology**: React 18, TypeScript, Vite, Ant Design
- **Deployment**: Nginx serving static files
- **Communication**: REST API, WebSocket for real-time updates

### Backend API (FastAPI)
- **Purpose**: Core business logic and API endpoints
- **Technology**: Python 3.12, FastAPI, SQLAlchemy, Pydantic
- **Responsibilities**:
  - User authentication and authorization
  - CRUD operations for all entities
  - Business rule validation
  - Audit logging
  - Task dispatching to Celery

### Calculation Engine (Celery)
- **Purpose**: Execute long-running actuarial calculations
- **Technology**: Python, Celery, NumPy, SciPy, Pandas
- **Responsibilities**:
  - Actuarial projections and valuations
  - Report generation
  - Data imports (large files)
  - Scheduled jobs
  - Experience analysis

### AI Service (Optional)
- **Purpose**: AI/ML features that augment user workflows
- **Technology**: Python, FastAPI, OpenAI API, sentence-transformers
- **Responsibilities**:
  - Natural language query processing
  - Document OCR and entity extraction
  - Anomaly detection
  - Semantic search
  - Narrative generation
- **Note**: Can be disabled without affecting core functionality

## Data Flow

### Request Flow
```
User Action → Frontend → Backend API → Database
                           ↓
                      Validation
                           ↓
                      Authorization
                           ↓
                      Business Logic
                           ↓
                      Audit Log
                           ↓
                      Response
```

### Calculation Flow
```
User triggers calculation → Backend creates CalculationRun record
                               ↓
                          Dispatches Celery task
                               ↓
                          Worker picks up task
                               ↓
                          Loads model, assumptions, policies
                               ↓
                          Executes calculation graph
                               ↓
                          Stores results in database
                               ↓
                          Updates run status
                               ↓
                          Sends WebSocket notification
                               ↓
                          User sees completion in UI
```

### AI Query Flow
```
User natural language query → Backend AI endpoint
                                  ↓
                             AI Service
                                  ↓
                             Parse intent & entities
                                  ↓
                             Generate structured query
                                  ↓
                             Execute against database
                                  ↓
                             Format response
                                  ↓
                             Return to user
```

## Database Schema Overview

### Core Entities
- **Users & Roles**: Authentication and authorization
- **Policies**: Insurance policy data
- **Policyholders**: Policy owner information
- **Claims**: Claim records and processing

### Actuarial Entities
- **AssumptionSets**: Versioned assumption collections
- **AssumptionTables**: Individual tables (mortality, lapse, etc.)
- **ModelDefinitions**: Calculation model configurations
- **CalculationRuns**: Execution records
- **CalculationResults**: Detailed output data

### Operational Entities
- **Tasks**: Workflow tasks and approvals
- **Notifications**: User notifications
- **AuditLog**: Immutable audit trail
- **ScheduledJobs**: Automation configuration

## Security Architecture

### Authentication
- Keycloak for enterprise SSO (production)
- JWT tokens for API authentication
- Refresh token rotation

### Authorization
- Role-Based Access Control (RBAC)
- Permission-based resource access
- Row-level security where applicable

### Data Protection
- TLS encryption in transit
- Encryption at rest for sensitive data
- Audit logging of all data access
- Soft deletes for data retention

## Scalability

### Horizontal Scaling
- Stateless backend API (scale via replicas)
- Celery workers (scale based on queue depth)
- Read replicas for database

### Performance Optimizations
- Redis caching for frequent queries
- Database connection pooling
- Elasticsearch for search offloading
- Calculation result partitioning

## Deployment Options

### Development
- Docker Compose for local development
- All services on single machine

### Production
- Kubernetes for orchestration
- Managed database services (RDS, Cloud SQL)
- Auto-scaling based on load
- Multi-AZ for high availability
