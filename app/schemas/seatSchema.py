from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

class seatBase(BaseModel):
    seat_number: str 
    screen_number: int 
    is_available: bool
    theatre_id: int 


class seatCreate(seatBase):
    pass


class seatUpdate(seatBase):
    pass

class seatOut(seatBase):
    id: int

    class Config:
        from_attribute = True
    