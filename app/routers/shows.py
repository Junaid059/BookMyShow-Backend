from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import models
from ..db import get_db
from ..schemas.showSchema import ShowCreate, ShowUpdate,ShowResponse
from ..auth import getCurrentUser


router = APIRouter()

@router.post("/createShows",response_model = ShowResponse)
def createShow(show: ShowCreate,db: Session = Depends(get_db),getcurrentuser: dict = Depends(getCurrentUser)):
    if getcurrentuser['role'] not in ('admin', 'organizer'):
        raise HTTPException(status_code=403,detail="Only admin and organizer can create shows")
    newShow = models.Show(show_time = show.show_time,price = show.price,screen_number = show.screen_number,movie_id = show.movie_id,theatre_id = show.theatre_id)
    db.add(newShow)
    db.commit()
    db.refresh(newShow)
    return newShow

@router.get("/getShows", response_model = list[ShowResponse])
def setShows(db: Session = Depends(get_db)):
    shows = db.query(models.Show).all()
    return shows

@router.get("/getShowbyId/{show_id}", response_model = ShowResponse)
def getShowbyId(show_id: int, db: Session = Depends(get_db)):
    show = db.query(models.Show).filter(models.Show.id == show_id).first()
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")
    return show

@router.put("/updateShow/{show_id}", response_model=ShowResponse)
def updateShow(show_id: int, show: ShowUpdate, db: Session = Depends(get_db), getcurrentuser = getCurrentUser):
    if getcurrentuser['role'] not in ('admin', 'organizer'):
        raise HTTPException(status_code=403, detail="Only admin and organizer can update shows")
    existingShow = db.query(models.Show).filter(models.Show.id == show_id).first()
    if not existingShow:
        raise HTTPException(status_code=404, detail="Show not found")
    setattr(existingShow, 'show_time', show.show_time)
    setattr(existingShow, 'price', show.price)
    setattr(existingShow, 'screen_number', show.screen_number)
    setattr(existingShow, 'movie_id', show.movie_id)
    setattr(existingShow, 'theatre_id', show.theatre_id)
    db.commit()
    db.refresh(existingShow)
    return existingShow

@router.delete("/deleteShow/{show_id}", response_model = ShowResponse)
def deleteShow(show_id: int, db: Session  =Depends(get_db), getcurrentuser = getCurrentUser):
    if getcurrentuser['role'] not in ('admin', 'organizer'):
        raise HTTPException(status_code=403, detail="Only admin and organizer can delete shows")
    existingShow = db.query(models.Show).filter(models.Show.id == show_id).first()
    if not existingShow:
        raise HTTPException(status_code=404, detail="Show not found")
    db.delete(existingShow)
    db.commit()
    return existingShow


