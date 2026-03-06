from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

class PaymentBase(BaseModel):
    amount: float = Field(..., gt=0, description="The amount to be paid")
    method: str = Field(..., description="The payment method (e.g., credit card, PayPal)")
    status: str = Field(default="pending", description="The status of the payment")
    booking_id: int = Field(..., description="The ID of the associated booking")

    @field_validator('status')
    @classmethod
    def validateStatus(cls,value):
        allowed_statuses = ['pending', 'completed', 'failed']
        if value not in allowed_statuses:
            raise ValueError(f"Status must be one of {allowed_statuses}")
        return value
    
    @field_validator('method')
    @classmethod
    def validateMethod(cls,value):
        allowed_methods = ['creditCard','bankTransfer','easyPaisa','jazzCash']
        if value not in allowed_methods:
            raise ValueError(f"Method must be one of {allowed_methods}")
        return value
    

class PaymentCreate(PaymentBase):
    pass

class paymentResponse(PaymentBase):
    id: int
    payment_date: str

    class Config:
        from_attribute = True
