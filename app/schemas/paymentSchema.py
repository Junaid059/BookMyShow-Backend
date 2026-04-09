from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class PaymentBase(BaseModel):
    amount: float = Field(..., gt=0)
    payment_method: str
    status: str = Field(default="pending")
    booking_id: int

    @field_validator('status')
    @classmethod
    def validateStatus(cls,value):
        allowed_statuses = ['pending', 'completed', 'failed']
        if value not in allowed_statuses:
            raise ValueError(f"Status must be one of {allowed_statuses}")
        return value
    
    @field_validator('payment_method')
    @classmethod
    def validateMethod(cls,value):
        allowed_methods = ['creditCard','bankTransfer','easyPaisa','jazzCash']
        if value not in allowed_methods:
            raise ValueError(f"Method must be one of {allowed_methods}")
        return value
    

class PaymentCreate(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    id: int
    payment_date: datetime

    class Config:
        from_attributes = True
