from pydantic import BaseModel, Field

class TheatreBase(BaseModel):
    name: str = Field(...,min_length=1,max_length=100)
    location: str = Field(...,min_length=1,max_length=200)
    city_id: int
    total_screens: int = Field(...,gt=0)

class TheatreCreate(TheatreBase):
    pass

class TheatreUpdate(TheatreBase):
    pass

class TheatreDelete(BaseModel):
    id: int

class TheatreResponse(TheatreBase):
    id: int

    class Config:
        from_attributes = True
