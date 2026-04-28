# How To Run The Fraud Detection System On Your Laptop

This guide is written for a Windows laptop and keeps the setup simple.

## 1. Install The Required Software

Install these first:

- Python 3.11 or above
- Git
- Docker Desktop
- VS Code or any code editor

## 2. Download The Project

```bash
git clone https://github.com/manvi0913/fraud-detection-system.git
cd fraud-detection-system/fraud-detection-api
```

## 3. Create A Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

## 4. Install Python Packages

```bash
pip install -r requirements.txt
```

## 5. Create The Environment File

Create a `.env` file inside `fraud-detection-api` and paste:

```env
APP_NAME=Fraud Detection System
DEBUG=true
API_V1_PREFIX=/api/v1
DATABASE_URL=mysql+pymysql://root:root@localhost:3306/fraud_detection
LOW_RISK_THRESHOLD=35
HIGH_RISK_THRESHOLD=70
```

## 6. Start MySQL Using Docker

```bash
docker compose up -d
```

## 7. Run The FastAPI Project

```bash
uvicorn app.main:app --reload
```

## 8. Open The Project In Browser

- Home: `http://127.0.0.1:8000/`
- Swagger API Docs: `http://127.0.0.1:8000/docs`
- Admin Dashboard: `http://127.0.0.1:8000/admin/dashboard`
- Health Check: `http://127.0.0.1:8000/health`
- Fraud Summary API: `http://127.0.0.1:8000/api/v1/fraud/summary`

## 9. Test The Main API

Use this sample payload in Swagger for `POST /api/v1/transactions`:

```json
{
  "external_id": "TXN-1001",
  "customer_id": "CUS-101",
  "amount": 24500,
  "currency": "INR",
  "merchant_name": "QuickPay Mall",
  "merchant_category": "electronics",
  "payment_channel": "online",
  "country": "IN",
  "card_present": false,
  "ip_address": "103.45.67.89",
  "device_id": "DEVICE-22A",
  "transaction_time": "2026-04-28T18:30:00"
}
```

## 10. Run The ML Module Separately

```bash
cd ..\fraud-detection-ml
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src/generate_dataset.py
python src/train_model.py
python src/evaluate_model.py
```
