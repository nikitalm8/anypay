from pydantic import BaseModel
from pydantic.fields import Field


class Rates(BaseModel):
    """
    Model of rates
    """

    in_: dict[str, float] = Field(..., alias='in')
    out: dict[str, float]
