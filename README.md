# Question-Answering Chatbot

## Overview

Enterprise-grade Question-Answering Chatbot for providing Supply Chain Intelligence using LLM-powered Retrieval Augmented Generation (RAG) with Agentic capabilities and Model Context Protocol (MCP).

### Key Features

#### 🤖 Agentic RAG (Retrieval Augmented Generation)
- **Intelligent Multi-Step Reasoning**: Automatically decomposes complex questions into focused sub-queries
- **Query Planning**: AI-powered analysis to break down questions into answerable components
- **Cross-Reference Verification**: Validates information across multiple sources
- **Reasoning Traces**: Provides transparent explanations of the agent's thought process
- **Adaptive Retrieval**: Dynamically adjusts search strategy based on query complexity

#### 🔍 Vector Search & Embeddings
- **Azure Cosmos DB Integration**: Native vector indexing with 1536-dimension embeddings
- **Semantic Similarity Search**: Goes beyond keyword matching to understand intent
- **Cosine Distance Function**: Optimized for Azure OpenAI ada-002 embeddings
- **Hybrid Search**: Combines vector search with fallback keyword search
- **Real-Time Indexing**: Documents are processed and searchable immediately after upload

#### 🌐 MCP (Model Context Protocol) Integration
- **4 Standardized Tools**: 
  - `search_documents`: Semantic search across SCIP knowledge base
  - `retrieve_context`: Depth-configurable context retrieval
  - `analyze_supply_chain`: Domain-specific supply chain analysis
  - `generate_insights`: AI-powered trend, risk, and opportunity identification
- **JSON-RPC Protocol**: Standard communication format for LLM interactions
- **Tool Orchestration**: Intelligent selection and chaining of tools

#### 📊 BASF SCIP Context
- **Sample Supply Chain Documentation**: 
  - Global procurement strategies and supplier diversification
  - Logistics network optimization across 80+ countries
  - Supplier performance management and KPIs
  - Inventory management with JIT and ABC analysis
- **Domain-Specific Prompts**: Tailored for BASF supply chain operations
- **SCIPPY Integration**: References to BASF's digital procurement platform
- **Real-World Metrics**: Actual performance targets and benchmarks

#### 🏭 Production-Ready Architecture
- **Comprehensive Health Checks**: Multi-level monitoring (basic, detailed, K8s probes)
- **Structured Logging**: JSON-formatted logs with correlation IDs
- **Error Handling**: Global exception handlers with graceful degradation
- **Security**: API key authentication, CORS configuration, input validation
- **Audit Logging**: Complete trail of queries and document access
- **Rate Limiting Ready**: Configured for production load management

#### 🚀 Additional Capabilities
- **FastAPI Backend**: High-performance async API with comprehensive endpoints
- **Streamlit Frontend**: Interactive UI for document upload and Q&A
- **Multi-Format Support**: PDF, DOCX, TXT, and Markdown documents
- **Conversation History**: Track and retrieve previous Q&A sessions
- **Source Citations**: Every answer includes references to source documents
- **Performance Metrics**: Real-time tracking of response times and accuracy

## Architecture

```
┌─────────────────┐
│   Streamlit UI  │
└────────┬────────┘
         │
    ┌────▼─────┐
    │  FastAPI │
    │  Backend │
    └────┬─────┘
         │
    ┌────▼──────────────────────┐
    │   Agentic RAG Pipeline    │
    │  ┌──────────────────────┐ │
    │  │  MCP Orchestrator    │ │
    │  └──────────────────────┘ │
    │  ┌──────────────────────┐ │
    │  │  Document Processor  │ │
    │  └──────────────────────┘ │
    │  ┌──────────────────────┐ │
    │  │  Vector Store        │ │
    │  └──────────────────────┘ │
    └────┬──────────────────────┘
         │
    ┌────▼────────────────┐
    │  Azure Cosmos DB    │
    │  (Vector Index)     │
    └─────────────────────┘
    ┌─────────────────────┐
    │  Azure OpenAI       │
    │  (GPT-4 + Embeddings)│
    └─────────────────────┘
```

## What's Included

This repository contains a complete, production-ready implementation:

### Backend (FastAPI)
- ✅ RESTful API with chat and document endpoints
- ✅ Azure Cosmos DB vector store with embeddings
- ✅ Azure OpenAI LLM and embedding integration
- ✅ RAG pipeline implementation
- ✅ Agentic RAG with query decomposition
- ✅ MCP (Model Context Protocol) server
- ✅ Health monitoring and logging
- ✅ BASF governance and compliance features

### Frontend (Streamlit)
- ✅ Interactive chat interface
- ✅ Document upload functionality
- ✅ Analytics dashboard
- ✅ Source citation display
- ✅ Agent reasoning visualization

### Data & Configuration
- ✅ 4 comprehensive SCIP sample documents
- ✅ Environment configuration template
- ✅ Initialization scripts
- ✅ Database setup automation

### DevOps & Deployment
- ✅ Docker & docker-compose files
- ✅ Comprehensive README
- ✅ Quick start guide
- ✅ Testing framework
- ✅ .gitignore and licensing

## Prerequisites

- Python 3.10+
- Azure subscription with:
  - Azure OpenAI Service
  - Azure Cosmos DB (with vector search capability)
- SCIP API access credentials
- Git

## Quick Start

### 1. Clone Repository

```bash
git clone <repository-url>
cd scip-qa-platform
```

### 2. Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Azure Credentials

```bash
# Copy environment template
cp .env.example .env  # Linux/Mac
copy .env.example .env  # Windows

# Edit .env with your Azure credentials
notepad .env  # Windows
nano .env     # Linux/Mac
```

**Required Configuration:**

```env
# Azure OpenAI (Required)
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002

# Azure Cosmos DB (Required)
COSMOS_DB_ENDPOINT=https://your-account.documents.azure.com:443/
COSMOS_DB_KEY=your-cosmos-key-here
COSMOS_DB_DATABASE_NAME=scip_knowledge_base
COSMOS_DB_CONTAINER_NAME=documents

# SCIP Configuration (Optional for demo)
SCIP_API_ENDPOINT=https://scip.basf.com/api
SCIP_API_KEY=your-scip-api-key
```

**How to Get Azure Credentials:**
1. **Azure OpenAI**: Go to [Azure Portal](https://portal.azure.com) → Azure OpenAI → Keys and Endpoint
2. **Cosmos DB**: Azure Portal → Cosmos DB → Keys → Primary Key and URI

### 4. Test Azure Connections

```bash
# Verify your Azure credentials work
python scripts/test_connection.py
```

Expected output:
```
✅ Azure OpenAI: Embeddings working
✅ Azure OpenAI: LLM working
✅ Cosmos DB: Connected
```

### 5. Initialize Database

```bash
# Create Cosmos DB database and container with vector indexing
python scripts/init_database.py
```

This creates:
- Database: `scip_knowledge_base`
- Container: `documents` with vector index
- Vector embedding policy for 1536-dimension embeddings

### 6. Load Sample Data

```bash
# Ingest sample SCIP supply chain documents
python scripts/ingest_sample_data.py
```

Ingests 4 sample documents:
- Global procurement strategies
- Logistics network optimization  
- Supplier performance management
- Inventory management practices

### 7. Start Services

**Terminal 1 - FastAPI Backend:**
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Streamlit Frontend:**
```bash
streamlit run frontend/app.py --server.port 8501
```

**Terminal 3 - MCP Server (Optional):**
```bash
python backend/mcp/server.py
```

### 8. Access Application

- **Streamlit UI**: http://localhost:8501 (Main user interface)
- **FastAPI Docs**: http://localhost:8000/docs (Interactive API documentation)
- **Health Check**: http://localhost:8000/health (System status)
- **Redoc**: http://localhost:8000/redoc (Alternative API docs)

### 9. Try It Out

**Ask Sample Questions:**
- "What is BASF's global procurement strategy?"
- "How many distribution centers does BASF operate?"
- "What are the key supplier evaluation criteria?"
- "Explain the inventory optimization approach"
- "What are the sustainability initiatives in logistics?"

### 10. Upload to GitHub

```bash
cd scip-qa-platform
git init
git add .
git commit -m "Initial commit: SCIP QA Platform v1.0"
git branch -M main
git remote add origin https://github.com/your-username/scip-qa-platform.git
git push -u origin main
```

**Important**: Ensure `.env` is in `.gitignore` to protect credentials!

## Project Structure

```
scip-qa-platform/
├── backend/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── chat.py           # Q&A endpoints
│   │   │   ├── documents.py      # Document management
│   │   │   └── health.py         # Health checks
│   │   └── dependencies.py       # Dependency injection
│   ├── core/
│   │   ├── config.py             # Configuration management
│   │   ├── logging.py            # Structured logging
│   │   └── security.py           # Authentication & authorization
│   ├── models/
│   │   ├── document.py           # Document models
│   │   ├── query.py              # Query models
│   │   └── response.py           # Response models
│   ├── services/
│   │   ├── embeddings.py         # Azure OpenAI embeddings
│   │   ├── llm.py                # LLM service
│   │   ├── vector_store.py       # Cosmos DB vector operations
│   │   ├── rag_pipeline.py       # RAG orchestration
│   │   └── agentic_rag.py        # Agentic RAG implementation
│   ├── mcp/
│   │   ├── server.py             # MCP server implementation
│   │   ├── tools.py              # MCP tools definition
│   │   └── protocol.py           # MCP protocol handlers
│   └── main.py                   # FastAPI application
├── frontend/
│   ├── app.py                    # Streamlit main app
│   ├── components/
│   │   ├── chat.py               # Chat interface
│   │   ├── upload.py             # Document upload
│   │   └── analytics.py          # Usage analytics
│   └── utils/
│       └── api_client.py         # Backend API client
├── data/
│   ├── sample/
│   │   ├── supply_chain_docs/    # Sample SCIP documents
│   │   └── procurement_data/     # Sample procurement data
│   └── schemas/
│       └── cosmos_schema.json    # Cosmos DB schema
├── scripts/
│   ├── init_database.py          # Database initialization
│   ├── ingest_sample_data.py     # Load sample data
│   └── test_connection.py        # Test Azure connections
├── tests/
│   ├── test_api.py               # API tests
│   ├── test_rag.py               # RAG pipeline tests
│   └── test_mcp.py               # MCP tests
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Container definition
├── docker-compose.yml            # Multi-container setup
└── README.md                     # This file
```

## Usage Examples

### 1. Ask Questions via UI

1. Navigate to http://localhost:8501
2. Enter your question in the chat interface
3. View AI-generated responses with source citations

### 2. Upload Documents

1. Click "Upload Documents" in sidebar
2. Select PDF, DOCX, or TXT files
3. Documents are automatically processed and indexed

### 3. API Usage

```python
import requests

# Ask a question
response = requests.post(
    "http://localhost:8000/api/v1/chat/ask",
    json={
        "question": "What are the latest supply chain trends?",
        "use_agentic": True,
        "max_sources": 5
    }
)

print(response.json())
```

## BASF Governance & Compliance

### Data Classification

All data is treated as **CONFIDENTIAL** by default. The platform implements:

- 🔒 **Access Control**: Role-based access to sensitive documents
- 📝 **Audit Logging**: Complete audit trail of all queries and access
- 🏷️ **Data Tagging**: Automatic classification of uploaded documents
- 🛡️ **Encryption**: Data encrypted at rest and in transit

### Compliance Features

- **GDPR Compliance**: Data retention policies and right to deletion
- **SOX Compliance**: Audit trails for financial data queries
- **BASF Standards**: Adherence to BASF's data governance policies

## MCP (Model Context Protocol)

The platform implements MCP for standardized LLM interactions:

```python
# MCP tools available:
- search_documents: Semantic search across SCIP data
- retrieve_context: Get relevant context for queries
- analyze_supply_chain: Domain-specific analysis
- generate_insights: AI-powered insight generation
```

## Agentic RAG Capabilities

The agentic RAG system can:

1. **Plan**: Break down complex questions into sub-queries
2. **Research**: Gather information from multiple sources
3. **Synthesize**: Combine information intelligently
4. **Verify**: Cross-check facts across documents
5. **Cite**: Provide source references for all claims

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'azure'`
```bash
pip install -r requirements.txt --upgrade
```

**Issue**: Cosmos DB connection timeout
- Check firewall rules in Azure Portal
- Verify COSMOS_DB_ENDPOINT and COSMOS_DB_KEY
- Ensure network connectivity to Azure

**Issue**: OpenAI rate limit exceeded
- Implement request throttling
- Check quota in Azure Portal
- Consider upgrading Azure OpenAI tier

### Logs

View application logs:
```bash
# Backend logs
tail -f logs/backend.log

# Streamlit logs
tail -f logs/streamlit.log
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov=frontend

# Run specific test
pytest tests/test_rag.py -v
```

### Code Quality

```bash
# Format code
black .

# Lint code
ruff check .

# Type checking
mypy backend/
```

## Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Azure Deployment

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed Azure deployment instructions.

## Performance Optimization

- **Caching**: Redis cache for frequent queries (configurable)
- **Batch Processing**: Bulk document ingestion
- **Async Operations**: Non-blocking I/O for API calls
- **Connection Pooling**: Efficient database connections

## Monitoring

- **Prometheus Metrics**: Available at `/metrics`
- **Health Endpoints**: `/health`, `/health/db`, `/health/openai`
- **Structured Logging**: JSON logs for easy parsing

## Security

- API key authentication
- Rate limiting on endpoints
- Input validation and sanitization
- CORS configuration
- Secret management via environment variables

## Contributing

1. Create feature branch: `git checkout -b feature/new-feature`
2. Make changes and commit: `git commit -am 'Add new feature'`
3. Push to branch: `git push origin feature/new-feature`
4. Create Pull Request

## License

Proprietary - BASF SE

## Support

For issues or questions:
- Internal BASF Support: scip-support@basf.com
- Documentation: https://scip.basf.com/docs
- SCIPPY Library: https://github.com/basf/scippy

## Acknowledgments

Built with:
- FastAPI & Streamlit
- Azure OpenAI & Cosmos DB
- LangChain
- Model Context Protocol (MCP)

---

**Version**: 1.0.0  
**Last Updated**: January 2026  
**Maintainer**: BASF Digital Supply Chain Team


