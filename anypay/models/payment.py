from datetime import datetime

from pydantic import BaseModel
from pydantic.fields import Field


class Payment(BaseModel):

    id: int = Field(..., alias='transaction_id')
    pay_id: int
    status: str
    method: str
    amount: int | float
    currency: str
    profit: int | float
    email: str
    description: str = Field(..., alias='desc')
    date: str
    pay_date: str
