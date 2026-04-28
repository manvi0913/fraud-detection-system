from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(tags=["Dashboard"])
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parents[2] / "templates"))


@router.get("/admin/dashboard")
def admin_dashboard(request: Request):
    metrics = {
        "transactions_today": "10,482",
        "high_risk_alerts": 128,
        "review_queue": 64,
        "latency_ms": 184,
        "reliability": "95.8%",
        "detection_uplift": "30%",
    }
    alerts = [
        {
            "external_id": "TXN-24081",
            "customer_id": "CUS-8892",
            "score": 91,
            "reason": "Country mismatch + device change + high amount",
            "status": "Blocked",
        },
        {
            "external_id": "TXN-24079",
            "customer_id": "CUS-1044",
            "score": 83,
            "reason": "High velocity + odd-hour activity",
            "status": "Under Review",
        },
        {
            "external_id": "TXN-24066",
            "customer_id": "CUS-5510",
            "score": 76,
            "reason": "Merchant risk + daily volume spike",
            "status": "Blocked",
        },
    ]

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "generated_at": datetime.now().strftime("%d %B %Y, %I:%M %p"),
            "admin_name": "Manvi Shukla",
            "metrics": metrics,
            "alerts": alerts,
        },
    )
