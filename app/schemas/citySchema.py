from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

class CityBase(BaseModel):
    name: str 
    state: str
    theatres: list[int] = Field(default_factory=list)

class CityCreate(CityBase):
    pass

class CityUpdate(CityBase):
    pass

class CityResponse(CityBase):
    id: int

    class Config:
        from_attribute = True
