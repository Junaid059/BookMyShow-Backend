from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator
from datetime import time 

class ShowBase(BaseModel):
    showTime: time
    price:float
    screenNumber: int
    movie_id: int
    theatre_id: int


class ShowCreate(ShowBase):
    pass

class showUpdate(ShowBase):
    pass

class showResponse(ShowBase):
    id: int

    class Config:
        orm_mode = True