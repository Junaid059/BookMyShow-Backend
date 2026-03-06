from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
import re

class UserBase(BaseModel):
    name: str = Field(...,min_length=1,max_length=100)
    email: EmailStr = Field(...,max_length=100)
    password: str = Field(...,min_length=6)
    role: Optional[str] = Field(default="user")

    @field_validator('email')
    @classmethod

    def validateEmail(cls,value):
        allowed = r"gmail,com,yahoo.com,hotmail.com,outlook.com,icloud.com,aol.com,protonmail.com,zoho.com,mail.com,gmx.com,yandex.com"
        if re.search(allowed, value):
            raise ValueError("Email domain not allowed")
        return value
    
    @field_validator('password')
    @classmethod
    def validatePassword(cls,value):
        if not re.search(r'[A-Z]',value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]',value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r'[0-9]',value):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]',value):
            raise ValueError("Password must contain at least one special character")
        return value    
     
    @field_validator('role')
    @classmethod
    def validateRole(cls,value):
        if value not in ['user,admin,organizer']:
            raise ValueError("Role must be either user, admin or organizer")
        return value
    

class UserCreate(UserBase):
    pass  


class UserLogin(BaseModel):
    email: EmailStr = Field(...,max_length=100)
    password: str = Field(...,min_length=6)

class UserUpdate(BaseModel):
    name:str = Field(...,min_length=1,max_length=100)
    email:EmailStr = Field(...,max_length=100)
    password:str = Field(...,min_length=6)

class UserDelete(BaseModel):
    email:EmailStr = Field(...,max_length=100)        
    
class UserResponse(BaseModel):
    id:int
    name:str
    email:EmailStr
    role:str
    created_at:str

    class config:
        from_attribute = True

