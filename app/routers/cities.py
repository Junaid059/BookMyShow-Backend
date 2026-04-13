from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import models
from ..db import get_db
from ..schemas.citySchema import CityCreate, CityResponse
from ..auth import getCurrentUser

router = APIRouter()

@router.post("/createCity", response_model = CityResponse)
def createCity(city: CityCreate, db: Session = Depends(get_db), getcurrentuser : dict = Depends(getCurrentUser)):
    if getcurrentuser['role'] not in ('admin', 'organizer'):
        raise HTTPException(status_code=403, detail="Only admin and organizer can create cities")
    newCity = models.City(name = city.name, state = city.state)
    db.add(newCity)
    db.commit()
    db.refresh(newCity)
    return newCity

@router.get("/getCities", response_model = list[CityResponse])
def getCities(db: Session = Depends(get_db)):
    cities = db.query(models.City).all()
    return cities

@router.get("/getCitybyId/{city_id}", response_model = CityResponse)
def getCitybyId(city_id: int, db: Session =  Depends(get_db)):
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city

@router.put("/updateCity/{city_id}", response_model=CityResponse)
def updateCityDetails(city_id: int, City: CityCreate, db: Session = Depends(get_db), getcurrentuser: dict = Depends(getCurrentUser)):
    if getcurrentuser['role'] not in ('admin', 'organizer'):
        raise HTTPException(status_code=403, detail="Only admin and organizer can update cities")
    existingCity = db.query(models.City).filter(models.City.id == city_id).first()
    if not existingCity:
        raise HTTPException(status_code=404, detail="City not found")
    setattr(existingCity, 'name', City.name)
    setattr(existingCity, 'state', City.state)
    db.commit()
    db.refresh(existingCity)
    return existingCity

@router.delete("/deleteCity/{city_id}", response_model = CityResponse)
def deleteCity(city_id: int, db: Session = Depends(get_db), getcurrentuser: dict = Depends(getCurrentUser)):
    if getcurrentuser['role'] not in ('admin', 'organizer'):
        raise HTTPException(status_code=403, detail="Only admin and organizer can delete cities")
    existingCity = db.query(models.City).filter(models.City.id  == city_id).first()
    if not existingCity:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(existingCity)
    db.commit()
    return existingCity

