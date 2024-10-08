from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt, Extra


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        # запрет принимать параметры, которые не описаны в схеме
        extra = Extra.forbid


class DonationCreate(DonationBase):
    pass


class DonationShortDB(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationFullDB(DonationShortDB):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
