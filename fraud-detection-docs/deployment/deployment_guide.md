# Deployment Guide

## Local Deployment

```bash
pip install -r requirements.txt
docker compose up -d
uvicorn app.main:app --reload
```

Open Swagger documentation at `http://127.0.0.1:8000/docs`.
