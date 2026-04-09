from fastapi import HTTPException, status, Depends,APIRouter
from sqlalchemy.orm import Session
from .models import models
from .db import get_db
from .auth import getCurrentUser,blacklistToken,accessToken,refreshToken
from .utils import  verify_password,hash_Password
from .schemas.userSchema import UserCreate, UserLogin, UserResponse, LoginResponse, LogoutResponse

router = APIRouter()

@router.post("/register",response_model = UserResponse)
def registerUser(user: UserCreate, db: Session = Depends(get_db)):
    existingUser = db.query(models.User).filter(models.User.email == user.email).first()
    if existingUser:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "User already exists")
    newUser = models.User(name = user.name, email = user.email, password = hash_Password(user.password), role = user.role)
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser

@router.post("/login",response_model = LoginResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    existingUser = db.query(models.User).filter(models.User.email == user.email).first()
    if not existingUser or not verify_password(user.password, str(existingUser.password)):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid email or password")
    token_data = {"id": existingUser.id, "role": existingUser.role}
    access = accessToken(token_data)
    refresh = refreshToken(token_data)
    return {"message": "Login successful", "access_token": access, "refresh_token": refresh, "token_type": "bearer"}


@router.post("/logout",response_model = LogoutResponse)
def logout(currentUser: dict = Depends(getCurrentUser)):
    jti = currentUser["jti"]
    blacklistToken(jti)
    return {"message":"Successfully logged out"}
