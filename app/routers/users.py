from fastapi import Depends,HTTPException,status,APIRouter
from sqlalchemy.orm import Session
from ..schemas import userSchema
from ..models import models
from ..db import get_db
from ..utils import hash_Password
from ..auth import getCurrentUser

router = APIRouter()

@router.post("/createUser",response_model = userSchema.UserResponse)
def createUser(user: userSchema.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "User already exists")
    hashed_pw = hash_Password(user.password)
    new_user = models.User(name = user.name, email = user.email, password = hashed_pw, role = user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 


@router.get("/getUsers" ,response_model = list[userSchema.UserResponse])
def getUsers(getcurrentuser: dict= Depends(getCurrentUser),db: Session = Depends(get_db)):
    if getcurrentuser['role'] != 'admin':
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Only admins can access this resource")
    users = db.query(models.User).all()
    return users

@router.get("/getUser/{user_id}",response_model = userSchema.UserResponse)
def SingleUser(user_id: int,getcurrentuser : dict = Depends(getCurrentUser),db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user and getcurrentuser['role'] != 'admin':
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found or you don't have permission to access this resource")
    return user

@router.put("/updateUser/{user_id}",response_model=userSchema.UserResponse)
def updateUser(user_id: int, user: userSchema.UserUpdate,db:Session = Depends(get_db)):
    user_to_update = db.query(models.User).filter(models.User.id == user_id).first()
    if not user_to_update:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found")
    setattr(user_to_update, "name", user.name)
    setattr(user_to_update, "email", user.email)
    setattr(user_to_update, "password", hash_Password(user.password))
    db.commit()
    db.refresh(user_to_update)
    return user_to_update

@router.delete("/deleteUser/{user_id}",response_model = userSchema.UserDelete)
def deleteUser(user_id: int, db: Session = Depends(get_db)):
    user_to_delete = db.query(models.User).filter(models.User.id == user_id).first()
    if not user_to_delete:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found")
    db.delete(user_to_delete)
    db.commit()
    return user_to_delete


# @router.get("/profile",response_model=userSchema.UserResponse)
# def getProfile(currentUser: dict = Depends(getCurrentUser), db: Session = Depends(get_db)):
#     user_id = currentUser["id"]
#     user = db.query(models.User).filter(models.User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found")
#     return user