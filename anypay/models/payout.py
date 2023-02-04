from typing import Union

from pydantic import BaseModel
from pydantic.fields import Field


class Payout(BaseModel):
    """
    Class for Payout model
    `date` and `complete_date` are dates in format: 'DD.MM.YYYY HH:MM:SS' or blank strings
    `exchange_rate` is float or None if payout was made in native currency
    """

    id: int = Field(..., alias='payout_id')
    transaction_id: int
    payout_type: str
    status: str
    amount: Union[int, float]
    commission: Union[int, float]
    commission_type: str
    exchange_rate: Union[int, float, None] = Field(None, alias='rate')
    wallet: int
    date: str
    complete_date: str
