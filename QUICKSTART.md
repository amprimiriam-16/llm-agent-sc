# Quick Start Guide

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.10 or higher
- ✅ Azure subscription with:
  - Azure OpenAI Service deployed
  - Azure Cosmos DB with vector search enabled
- ✅ Git installed

## Installation Steps

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd scip-qa-platform
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
# Copy template
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Edit .env with your credentials
notepad .env  # Windows
nano .env     # Linux/Mac
```

**Required Settings:**
```
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-key-here
COSMOS_DB_ENDPOINT=https://your-account.documents.azure.com:443/
COSMOS_DB_KEY=your-key-here
```

### 5. Test Connections
```bash
python scripts/test_connection.py
```

### 6. Initialize Database
```bash
python scripts/init_database.py
```

### 7. Load Sample Data
```bash
python scripts/ingest_sample_data.py
```

### 8. Start Services

**Terminal 1 - Backend:**
```bash
python -m uvicorn backend.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
streamlit run frontend/app.py
```

### 9. Access Application
- Frontend UI: http://localhost:8501
- API Docs: http://localhost:8000/docs

## Docker Quick Start

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Troubleshooting

**Issue: ModuleNotFoundError**
```bash
pip install -r requirements.txt --upgrade
```

**Issue: Azure connection failed**
- Verify credentials in .env
- Check Azure Portal for service status
- Ensure firewall allows connections

**Issue: Port already in use**
```bash
# Change port in .env
API_PORT=8001
STREAMLIT_PORT=8502
```

## Next Steps
- Upload your own documents
- Customize system prompts
- Configure additional settings
- Deploy to production
