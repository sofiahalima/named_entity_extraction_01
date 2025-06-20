# Named Entity Extraction Pipeline with NLP + Azure

This project implements an end-to-end Named Entity Recognition (NER) pipeline using a fine-tuned spaCy model & BERT Model, Azure Blob Storage for document ingestion, Azure Cosmos DB for storage, and FastAPI for serving results via an API, Azure App Services & Github Actions for deployment & scaling.

---

## 🚀 Features
- Load documents from Azure Blob Storage
- Extract named entities using a custom spaCy NER model
- Store raw + enriched documents in Azure Cosmos DB
- Expose extracted entities via a FastAPI API endpoint
- Search entities by label, date, and keyword

---

## 📁 Project Structure
```
EntityExtractionDemo/
├── app/
│   ├── service/
│   │   ├── main.py           # FastAPI app
│   │   ├── db.py             # Cosmos DB interaction
│   │   ├── data_collection_utility.py    # Blob ingestion logic
│   │   ├── ner.py            # spaCy NER logic
│   │   ├── search.py         # Search API
│   │   |── run_pipeline.py   # Batch processor
│   └── __init__.py
├   |
|   └── model/output         # Trained spaCy model
├── .env                      # Environment variables
├── Dockerfile                # Docker config
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── .github/workflows/deploy.yml # GitHub Actions CI : to azure App Service
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/sofiahalima/named_entity_extraction_01.git
cd named_entity_extraction_01
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create a `.env` File
```
AZURE_BLOB_CONNECTION_STRING=your-connection-string
AZURE_BLOB_CONTAINER_NAME=your-container-name
COSMOS_DB_URL=your-cosmos-url
COSMOS_DB_KEY=your-cosmos-key
COSMOS_DB_NAME=ner_pipeline
COSMOS_CONTAINER_NAME=documents
PROJECT_ROOT = your root folder
```

---

## 📦 Run the NER Pipeline
```bash
python pipeline/run_pipeline.py
```

---

## 🌐 Start the FastAPI Server
```bash
python -m uvicorn app.service.main:app --reload
```

Then open: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Example API Calls
- `GET /entities?id=doc-123` – Get NER results by document ID
- `GET /search?label=person&start_date=2025-01-01&keyword=climate` – Search by filters :TODO( Search by keyword & date)

---

## 🐳 Docker Usage :TODO (planned to deploy to Azure App Services)
```bash
docker build -t ner-api .
docker run -p 8000:8000 --env-file .env ner-api
```

---

## ✅ GitHub Actions CI/CD
- Located at `.github/workflows/deploy.yml`  
- Linting and dependency check on every `.github/workflows/lint.yml`

---

## 📌 Notes
- Make sure your spaCy model is saved to `app/model/output/`
- All folders contain `__init__.py` to ensure package resolution
- Supports Cosmos DB SQL API only

---
