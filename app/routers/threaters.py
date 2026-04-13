from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import models
from ..db import get_db
from ..schemas.TheatreSchema import TheatreCreate, TheatreResponse
from ..auth import getCurrentUser

router =  APIRouter()

