from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.schemas.transaction import SummaryItem


def build_summary(db: Session) -> SummaryItem:
    totals = (
        db.query(
            func.count(Transaction.id),
            func.coalesce(func.avg(Transaction.risk_score), 0.0),
            func.sum(case((Transaction.risk_label == "low", 1), else_=0)),
            func.sum(case((Transaction.risk_label == "medium", 1), else_=0)),
            func.sum(case((Transaction.risk_label == "high", 1), else_=0)),
            func.sum(case((Transaction.status == "blocked", 1), else_=0)),
        )
        .one()
    )

    return SummaryItem(
        total_transactions=int(totals[0] or 0),
        average_risk_score=round(float(totals[1] or 0.0), 2),
        low_risk_count=int(totals[2] or 0),
        medium_risk_count=int(totals[3] or 0),
        high_risk_count=int(totals[4] or 0),
        blocked_transactions=int(totals[5] or 0),
    )
