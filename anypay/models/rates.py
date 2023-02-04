from typing import Dict

from pydantic import BaseModel
from pydantic.fields import Field


class Rates(BaseModel):
    """
    Model of rates
    """

    in_: Dict[str, float] = Field(..., alias='in')
    out: Dict[str, float]
