from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator


class ReviewBase(BaseModel):
    rating: int= Field(..., ge=1, le=5, description="Rating must be between 1 and 5")
    comment: str= Field(..., max_length=500, description="Comment cannot exceed 500 characters")
    user_id: int
    movie_id: int

    @field_validator('rating')
    @classmethod
    def validate_rating(cls, value):
        if not (1 <= value <= 5):
            raise ValueError('Rating must be between 1 and 5')
        return value
    
    @field_validator('comment')
    @classmethod
    def validateComment(cls,value):
        if len(value)> 500:
            raise ValueError('Comment cannot exceed 500 characters')
        return value
    
class ReviewResponse(ReviewBase):
    id: int
    created_at: str

class ReviewCreate(ReviewBase):
    pass

    class Config:
        from_attributes = True

