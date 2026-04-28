# Fraud Detection API

The backend service for the Fraud Detection System is a **FastAPI + MySQL** application that receives financial transactions, calculates a fraud risk score, stores the results, and exposes monitoring endpoints.

## Project Highlights

- Built with **FastAPI**, **SQLAlchemy**, and **MySQL**
- Supports **real-time transaction ingestion**
- Generates fraud risk scores using **multi-factor decision logic**
- Designed around **4 core REST APIs**
- Includes **unit tests**, **Docker Compose**, and **GitHub Actions CI**

## Core REST APIs

1. `POST /api/v1/transactions`
2. `POST /api/v1/fraud/score`
3. `GET /api/v1/transactions/{external_id}`
4. `GET /api/v1/fraud/summary`

Additional utility endpoints include `GET /health` and `GET /api/v1/transactions`.

## Local Setup

```bash
pip install -r requirements.txt
docker compose up -d
uvicorn app.main:app --reload
```

Open Swagger UI at `http://127.0.0.1:8000/docs`.
