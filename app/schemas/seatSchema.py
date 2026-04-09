from pydantic import BaseModel

class SeatBase(BaseModel):
    seat_number: str 
    screen_number: int 
    is_available: bool = True
    theatre_id: int 


class SeatCreate(SeatBase):
    pass

class SeatUpdate(SeatBase):
    pass

class SeatResponse(SeatBase):
    id: int

    class Config:
        from_attributes = True
    