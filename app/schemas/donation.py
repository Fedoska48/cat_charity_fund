from pydantic import BaseModel, Field


class DonationBase(BaseModel):
    ...


class DonationCreate(DonationBase):
    ...


class DonationUpdate(DonationBase):
    ...


class DonationDB(DonationBase):
    ...
