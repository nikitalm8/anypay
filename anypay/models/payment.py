from typing import Union, Optional

from pydantic import BaseModel
from pydantic.fields import Field


class Payment(BaseModel):
    """
    Class for Payment model
    `date` and `pay_date` are dates in format: 'DD.MM.YYYY HH:MM:SS' or blank strings
    """

    id: int = Field(..., alias='pay_id')
    transaction_id: int
    status: str
    method: str
    amount: Union[int, float]
    currency: str
    profit: Union[int, float]
    email: str
    description: str = Field(..., alias='desc')
    date: str
    pay_date: Optional[str] = None
