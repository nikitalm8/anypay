from datetime import datetime

from pydantic import BaseModel
from pydantic.fields import Field


class Payout(BaseModel):

    id: int = Field(..., alias='transaction_id')
    payout_id: int
    payout_type: str
    status: str
    amount: int | float
    commission: int | float
    commission_type: str
    exchange_rate: int | float | None = Field(None, alias='rate')
    wallet: int
    date: str
    complete_date: str
