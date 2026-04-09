from pydantic import BaseModel
from datetime import datetime

class ShowBase(BaseModel):
    show_time: datetime
    price: float
    screen_number: int
    movie_id: int
    theatre_id: int


class ShowCreate(ShowBase):
    pass

class ShowUpdate(ShowBase):
    pass

class ShowResponse(ShowBase):
    id: int

    class Config:
        from_attributes = True