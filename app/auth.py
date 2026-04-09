from jwt import encode, decode,PyJWTError
from datetime import datetime, timedelta
from .models import models
from dotenv import load_dotenv
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
import os
import uuid

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
Algorithm = os.getenv('ALGORITHM')
Access_token_expire_minutes = 30
Access_token_expire_days = 7
Token_Type = HTTPBearer()
blaclisted_tokens = set()

if not SECRET_KEY or not Algorithm:
    raise ValueError("SECRET_KEY and ALGORITHM must be set in environment variables")


def accessToken(data: dict):
    to_encode = data.copy()
    jti = str(uuid.uuid4())
    expiry_date = datetime.utcnow() + timedelta(minutes=Access_token_expire_minutes)
    to_encode.update({"exp":expiry_date,"jti":jti})
    return encode(to_encode, SECRET_KEY or "", algorithm=Algorithm or "")
    
def refreshToken(data: dict):
    to_encode = data.copy()
    jti = str(uuid.uuid4())
    expiry = datetime.utcnow() + timedelta(days = Access_token_expire_days)
    to_encode.update({"exp":expiry, "jti":jti}) 
    return encode(to_encode, SECRET_KEY or "", algorithm=Algorithm or "")

def verifyToken(token: str):
    try:
        payload = decode(token,SECRET_KEY or "", algorithms = [Algorithm or ""])
        jti = payload.get("jti")
        id = payload.get("id")
        role = payload.get("role")
        if jti in blaclisted_tokens:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has been blacklisted") 
        if id is None or role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        return payload
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
def getCurrentUser(token: HTTPAuthorizationCredentials = Depends(Token_Type)):
    payload = verifyToken(token=token.credentials)
    user_id = payload.get("id")
    role = payload.get("role")
    jti = payload.get("jti")
    return {"id": user_id, "role": role, "jti": jti}   
    
def blacklistToken(token: str):
   return blaclisted_tokens.add(token)