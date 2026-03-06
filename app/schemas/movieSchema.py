from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator


class MovieBase(BaseModel):
    title: str = Field(...,min_length=1,max_length=200)
    description: str = Field(...,min_length=1,max_length=1000)
    duration: int = Field(...,gt=0)  # in minutes
    release_date: str = Field(...,pattern=r'^\d{4}-\d{2}-\d{2}$')  # YYYY-MM-DD
    genre:str = Field(...,min_length=1,max_length=100)
    rating:str = Field(...,min_length=1,max_length=10)

class MovieCreate(MovieBase):
    pass    

class MovieUpdate(MovieBase):
    pass

class MovieDelete(MovieBase):
    pass 

class MovieResponse(BaseModel):
    id:int
    title:str
    description:str
    duration:int
    release_date:str
    genre:str
    rating:str


    class config:
        from_attributes = True