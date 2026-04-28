from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.transaction import Transaction
from app.schemas.transaction import FraudScoreRequest, FraudScoreResponse, SummaryResponse, TransactionCreate, TransactionResponse
from app.services.dashboard import build_summary
from app.services.fraud_engine import FraudScorer


transaction_router = APIRouter(prefix="/transactions", tags=["Transactions"])
fraud_router = APIRouter(prefix="/fraud", tags=["Fraud"])
scorer = FraudScorer()


@transaction_router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(payload: TransactionCreate, db: Session = Depends(get_db)):
    existing = db.query(Transaction).filter(Transaction.external_id == payload.external_id).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Transaction with this external_id already exists.")

    context = scorer.build_context(db, payload)
    decision = scorer.score_transaction(payload, context)

    transaction = Transaction(
        external_id=payload.external_id,
        customer_id=payload.customer_id,
        amount=payload.amount,
        currency=payload.currency,
        merchant_name=payload.merchant_name,
        merchant_category=payload.merchant_category,
        payment_channel=payload.payment_channel,
        country=payload.country,
        card_present=payload.card_present,
        ip_address=payload.ip_address,
        device_id=payload.device_id,
        transaction_time=payload.transaction_time,
        risk_score=decision.risk_score,
        risk_label=decision.risk_label,
        recommended_action=decision.recommended_action,
        status="blocked" if decision.risk_label == "high" else "processed",
        risk_reasons=[reason.model_dump() for reason in decision.risk_reasons],
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


@transaction_router.get("/{external_id}", response_model=TransactionResponse)
def get_transaction(external_id: str, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.external_id == external_id).first()
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found.")
    return transaction


@transaction_router.get("", response_model=list[TransactionResponse])
def list_transactions(db: Session = Depends(get_db), risk_label: str | None = Query(default=None), limit: int = Query(default=20, ge=1, le=100)):
    query = db.query(Transaction).order_by(Transaction.created_at.desc())
    if risk_label:
        query = query.filter(Transaction.risk_label == risk_label)
    return query.limit(limit).all()


@fraud_router.post("/score", response_model=FraudScoreResponse)
def preview_fraud_score(payload: FraudScoreRequest, db: Session = Depends(get_db)):
    request_payload = TransactionCreate(**payload.model_dump())
    context = scorer.build_context(db, request_payload)
    return scorer.score_transaction(request_payload, context)


@fraud_router.get("/summary", response_model=SummaryResponse)
def get_summary(db: Session = Depends(get_db)):
    metrics = build_summary(db)
    recent_alerts = db.query(Transaction).filter(Transaction.risk_label == "high").order_by(Transaction.created_at.desc()).limit(5).all()
    return SummaryResponse(metrics=metrics, recent_alerts=recent_alerts)
