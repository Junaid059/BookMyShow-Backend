from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

class ThreaterBase(BaseModel):
    name: str = Field(...,min_length=1,max_length=100)
    location: str = Field(...,min_length=1,max_length=200)
    total_seats: int = Field(...,gt=0)

class ThreaterCreate(ThreaterBase):
    pass

class ThreaterUpdate(ThreaterBase):
    pass

class ThreaterDelete(ThreaterBase):
    pass

class ThreaterResponse(BaseModel):
    id: int
    name: str
    location: str
    total_seats: int

    class Config:
        from_attributes = True
