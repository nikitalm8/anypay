from pydantic import BaseModel
from pydantic.fields import Field


class Rates(BaseModel):

    in_: dict[str, float] = Field(..., alias='in')
    out: dict[str, float]
