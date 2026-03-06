from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

class NotificationBase(BaseModel):
    message: str = Field(...,max_length=255)
    user_id: int
    is_read: bool = Field(default=False)
    

    @field_validator('message')
    @classmethod
    def validateMessage(cls,value):
        if not value.strip():
            raise ValueError("Message cannot be empty or whitespace")
        return value
    

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(NotificationBase):
    pass
    
class NotificationRead(NotificationBase):
    id: int
    created_at: str
   
    class Config:
        from_attribute = True
