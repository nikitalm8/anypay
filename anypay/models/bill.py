from pydantic import BaseModel
from pydantic.fields import Field


class Bill(BaseModel):

    id: int = Field(..., alias='pay_id')
    transaction_id: int | None = None
    status: str = 'waiting'
    url: str = Field(..., alias='payment_url')
