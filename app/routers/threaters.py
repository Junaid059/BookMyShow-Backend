from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import models
from ..db import get_db
from ..schemas.TheatreSchema import TheatreCreate, TheatreResponse, TheatreUpdate
from ..auth import getCurrentUser

router =  APIRouter()

@router.post("/createThreater", response_model = TheatreResponse)
def createThreater(threater: TheatreCreate, db: Session = Depends(get_db), getcurrentuser: dict = Depends(getCurrentUser)):
    if getcurrentuser['role'] not in ('admin','organizer'):
        raise HTTPException(status_code=403, detail="Only admin and organizer can create threater")
    newThreater = models.Theatre(name = threater.name, location = threater.location, city_id = threater.city_id, total_screens = threater.total_screens)
    db.add(newThreater)
    db.commit()
    db.refresh(newThreater)
    return newThreater

@router.get("/getallThreater", response_model = list[TheatreResponse])
def getAllThreater(db: Session = Depends(get_db)):
    threaters = db.query(models.Theatre).all()
    return threaters

@router.get("/getThreater/{threater_id}", response_model = TheatreResponse)
def getThreaterbyId(threater_id: int, db: Session = Depends(get_db)):
    threater = db.query(models.Theatre).filter(models.Theatre.id == threater_id).first()
    if threater is None:
        raise HTTPException(status_code=404, detail="Threater not found")
    return threater

@router.put("/updateThreater/{threater_id}", response_model = TheatreResponse)
def updateThreater(threater_id: int, threater: TheatreUpdate,db: Session = Depends(get_db), getcurrentuser : dict= Depends(getCurrentUser)):
    if getcurrentuser['role'] not in ('admin','organizer'):
        raise HTTPException(status_code=403, detail="Only admin and organizer can update threater")
    threaterToUpdate = db.query(models.Theatre).filter(models.Theatre.id ==threater_id).first()
    if threaterToUpdate is None:
        raise HTTPException(status_code=404, detail="Threater not found")
    setattr(threaterToUpdate,'name', threater.name)
    setattr(threaterToUpdate,'location', threater.location)
    setattr(threaterToUpdate,'city_id', threater.city_id)
    setattr(threaterToUpdate,'total_screens', threater.total_screens)
    db.commit()
    db.refresh(threaterToUpdate)
    return threaterToUpdate

@router.delete("/deleteThreater/{threater_id}", response_model = TheatreResponse)
def deleteThreater(threater_id: int, db: Session = Depends(get_db), getcurrentuser: dict = Depends(getCurrentUser)):
    if getcurrentuser['role'] not in ('admin','organizer'):
        raise HTTPException(status_code=403, detail="Only admin and organizer can delete threater")
    threaterToDelete = db.query(models.Theatre).filter(models.Theatre.id == threater_id).first()
    if threaterToDelete is None:
        raise HTTPException(status_code=404, detail="Threater not found")
    db.delete(threaterToDelete)
    db.commit()
    return threaterToDelete

 
