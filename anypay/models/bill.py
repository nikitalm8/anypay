from typing import Union

from pydantic import BaseModel
from pydantic.fields import Field


class Bill(BaseModel):
    """
    Class for Bill model
    Due to strange API response, `status` does not represent the actual status of payment
    """

    id: int = Field(..., alias='pay_id')
    transaction_id: Union[int, None] = None
    status: str = 'waiting'
    url: str = Field(..., alias='payment_url')
