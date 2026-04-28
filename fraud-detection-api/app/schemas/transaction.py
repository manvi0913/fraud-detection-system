from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TransactionBase(BaseModel):
    external_id: str = Field(..., min_length=4, max_length=64)
    customer_id: str = Field(..., min_length=4, max_length=64)
    amount: float = Field(..., gt=0)
    currency: str = Field(..., min_length=3, max_length=8)
    merchant_name: str = Field(..., min_length=2, max_length=128)
    merchant_category: str = Field(..., min_length=2, max_length=64)
    payment_channel: str = Field(..., min_length=2, max_length=32)
    country: str = Field(..., min_length=2, max_length=8)
    card_present: bool = False
    ip_address: str = Field(..., min_length=7, max_length=64)
    device_id: str = Field(..., min_length=3, max_length=64)
    transaction_time: datetime


class TransactionCreate(TransactionBase):
    pass


class FraudScoreRequest(TransactionBase):
    pass


class RiskReason(BaseModel):
    factor: str
    weight: float
    description: str


class FraudScoreResponse(BaseModel):
    risk_score: float
    risk_label: str
    recommended_action: str
    risk_reasons: list[RiskReason]


class TransactionResponse(TransactionBase):
    id: int
    risk_score: float
    risk_label: str
    recommended_action: str
    status: str
    risk_reasons: list[RiskReason]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SummaryItem(BaseModel):
    total_transactions: int
    low_risk_count: int
    medium_risk_count: int
    high_risk_count: int
    blocked_transactions: int
    average_risk_score: float


class SummaryResponse(BaseModel):
    metrics: SummaryItem
    recent_alerts: list[TransactionResponse]
