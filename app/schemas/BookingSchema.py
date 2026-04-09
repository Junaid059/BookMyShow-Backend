from pydantic import BaseModel,Field
from datetime import datetime


class BookingBase(BaseModel):
    booking_date: datetime = Field(default_factory=datetime.utcnow)
    total_amount: float
    status: str = Field(default='pending')
    seat_numbers: str
    user_id: int
    show_id: int


class BookingCreate(BookingBase):
    pass


class BookingDelete(BaseModel):
    id: int

class BookingResponse(BookingBase):
    id: int

    class Config:
        from_attributes = True

