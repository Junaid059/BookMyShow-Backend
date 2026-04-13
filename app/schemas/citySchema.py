from pydantic import BaseModel

class CityBase(BaseModel):
    name: str 
    state: str
    threater: str

class CityCreate(CityBase):
    pass

class CityUpdate(CityBase):
    pass

class CityResponse(CityBase):
    id: int

    class Config:
        from_attributes = True
