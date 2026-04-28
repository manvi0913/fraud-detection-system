from collections import Counter
from dataclasses import dataclass
from datetime import timedelta

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.transaction import Transaction
from app.schemas.transaction import FraudScoreResponse, RiskReason, TransactionCreate


@dataclass
class RiskContext:
    recent_one_hour_count: int
    recent_twenty_four_hour_total: float
    known_country: str | None
    known_device: bool


class FraudScorer:
    HIGH_RISK_MERCHANTS = {"crypto", "gift_cards", "gaming", "travel"}

    def build_context(self, db: Session, payload: TransactionCreate) -> RiskContext:
        last_day = payload.transaction_time - timedelta(hours=24)
        one_hour = payload.transaction_time - timedelta(hours=1)

        history = (
            db.query(Transaction)
            .filter(
                Transaction.customer_id == payload.customer_id,
                Transaction.transaction_time >= last_day,
            )
            .order_by(Transaction.transaction_time.desc())
            .all()
        )

        recent_one_hour = [txn for txn in history if txn.transaction_time >= one_hour]
        country_counter = Counter(txn.country for txn in history)
        known_device = payload.device_id in {txn.device_id for txn in history}

        return RiskContext(
            recent_one_hour_count=len(recent_one_hour),
            recent_twenty_four_hour_total=sum(txn.amount for txn in history),
            known_country=country_counter.most_common(1)[0][0] if country_counter else None,
            known_device=known_device if history else True,
        )

    def score_transaction(self, payload: TransactionCreate, context: RiskContext) -> FraudScoreResponse:
        reasons: list[RiskReason] = []
        score = 5.0

        if payload.amount >= 50000:
            score += 25
            reasons.append(RiskReason(factor="high_amount", weight=25, description="Transaction amount is significantly above the normal monitoring threshold."))
        elif payload.amount >= 20000:
            score += 15
            reasons.append(RiskReason(factor="moderate_high_amount", weight=15, description="Transaction amount is higher than standard retail activity."))

        if context.recent_one_hour_count >= 5:
            score += 18
            reasons.append(RiskReason(factor="high_velocity", weight=18, description="Customer performed multiple transactions within the last hour."))

        if context.recent_twenty_four_hour_total + payload.amount >= 100000:
            score += 12
            reasons.append(RiskReason(factor="daily_volume_spike", weight=12, description="Customer's daily transaction volume is unusually high."))

        if context.known_country and context.known_country != payload.country:
            score += 20
            reasons.append(RiskReason(factor="country_mismatch", weight=20, description="Current transaction country differs from the customer's recent behavior."))

        if not context.known_device:
            score += 12
            reasons.append(RiskReason(factor="device_change", weight=12, description="The device ID has not been observed in the recent customer profile."))

        if not payload.card_present and payload.payment_channel.lower() in {"online", "upi", "wallet"}:
            score += 8
            reasons.append(RiskReason(factor="card_not_present", weight=8, description="Card-not-present transactions are typically more exposed to fraud risk."))

        if payload.merchant_category.lower() in self.HIGH_RISK_MERCHANTS:
            score += 10
            reasons.append(RiskReason(factor="merchant_risk", weight=10, description="Merchant category is frequently associated with fraudulent attempts."))

        if payload.transaction_time.hour < 5:
            score += 7
            reasons.append(RiskReason(factor="odd_hour_activity", weight=7, description="Transaction occurred during low-activity hours."))

        final_score = round(min(score, 99.0), 2)

        if final_score >= settings.high_risk_threshold:
            label = "high"
            action = "block"
        elif final_score >= settings.low_risk_threshold:
            label = "medium"
            action = "review"
        else:
            label = "low"
            action = "approve"

        return FraudScoreResponse(
            risk_score=final_score,
            risk_label=label,
            recommended_action=action,
            risk_reasons=reasons,
        )
