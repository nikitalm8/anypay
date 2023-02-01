from pydantic import BaseModel
from pydantic.fields import Field


class Bill(BaseModel):

    id: int = Field(..., alias='transaction_id')
    pay_id: int
    status: str = 'waiting'
    url: str = Field(..., alias='payment_url')
