from datetime import datetime

from app.schemas.transaction import TransactionCreate
from app.services.fraud_engine import FraudScorer, RiskContext


def build_payload(**overrides):
    payload = {
        "external_id": "TXN-1001",
        "customer_id": "CUS-1001",
        "amount": 65000,
        "currency": "INR",
        "merchant_name": "Rapid Crypto Hub",
        "merchant_category": "crypto",
        "payment_channel": "online",
        "country": "US",
        "card_present": False,
        "ip_address": "10.10.10.10",
        "device_id": "NEW-DEVICE-9",
        "transaction_time": datetime(2026, 4, 28, 2, 15, 0),
    }
    payload.update(overrides)
    return TransactionCreate(**payload)


def test_high_risk_transaction_is_blocked():
    scorer = FraudScorer()
    context = RiskContext(recent_one_hour_count=6, recent_twenty_four_hour_total=50000, known_country="IN", known_device=False)

    result = scorer.score_transaction(build_payload(), context)

    assert result.risk_label == "high"
    assert result.recommended_action == "block"
    assert result.risk_score >= 70


def test_low_risk_transaction_is_approved():
    scorer = FraudScorer()
    context = RiskContext(recent_one_hour_count=0, recent_twenty_four_hour_total=1500, known_country="IN", known_device=True)

    result = scorer.score_transaction(
        build_payload(amount=1200, merchant_category="groceries", payment_channel="pos", country="IN", card_present=True, transaction_time=datetime(2026, 4, 28, 14, 0, 0)),
        context,
    )

    assert result.risk_label == "low"
    assert result.recommended_action == "approve"
    assert result.risk_score < 35
