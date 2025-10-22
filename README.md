# ETL Sidecar - Embeddings Service

Python-based embeddings sidecar service for Smart-ETL semantic similarity calculations.

## Overview

This service provides semantic similarity scores for header-to-field mapping in the Smart-ETL pipeline using sentence transformers.

## Features

- FastAPI-based REST API
- Sentence transformer embeddings
- Semantic similarity calculations
- Health check endpoints
- Redis caching (optional)

## Setup

1. Create virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install fastapi uvicorn sentence-transformers numpy orjson scikit-learn
```

3. Run the service:
```bash
uvicorn app:app --host 0.0.0.0 --port 3009
```

## API Endpoints

- `GET /healthz` - Health check
- `POST /similarity/headers` - Calculate header similarities

## Development

The service runs on port 3009 and is accessible internally to the Smart-ETL Node.js service.


