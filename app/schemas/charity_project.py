from pydantic import BaseModel, Field


class CharityProjectBase(BaseModel):
    ...


class CharityProjectCreate(CharityProjectBase):
    ...


class CharityProjectUpdate(CharityProjectBase):
    ...


class CharityProjectDB(CharityProjectBase):
    ...
