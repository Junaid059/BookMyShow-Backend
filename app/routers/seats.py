from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import models
from ..db import get_db
from ..schemas.seatSchema import SeatCreate, SeatResponse, SeatUpdate
from ..auth import getCurrentUser

router = APIRouter()

@router.post("/createSeat", response_model = SeatResponse)
def createSeat(seat: SeatCreate, db: Session = Depends(get_db), getcurrentuser: dict = Depends(getCurrentUser)):
    if getcurrentuser['role'] not in ('admin', 'organizer'):
        raise HTTPException(status_code=403, detail="Only admin and organizer can create seat")
    newSeat = models.Seat(seat_number = seat.seat_number, screen_number = seat.screen_number, is_available = seat.is_available, theatre_id = seat.theatre_id)
    db.add(newSeat)
    db.commit()
    db.refresh(newSeat)
    return newSeat

@router.get("/getallSeats", response_model = list[SeatResponse])
def getAllSeat(db: Session = Depends(get_db)):
    seats = db.query(models.Seat).all()
    return seats

@router.get("/getSeat/{seat_id}", response_model = SeatResponse)
def getSeatbyId(seat_id: int, db:Session = Depends(get_db)):
    seat = db.query(models.Seat).filter(models.Seat.id == seat_id).first()
    if seat is None:
        raise HTTPException(status_code=404, detail="Seat not found")
    return seat

@router.put("/updateSeat/{seat_id}", response_model = SeatUpdate)
def updateSeat(seat_id: int, seat: SeatUpdate, db: Session = Depends(get_db), getcurrentuser: dict = Depends(getCurrentUser)):
    if getcurrentuser['role'] not in ('admin', 'organizer'):
        raise HTTPException(status_code=403, detail="Only admin and organizer can update seat")
    seatToUpdate = db.query(models.Seat).filter(models.Seat.id == seat_id).first()
    if seatToUpdate is None:
        raise HTTPException(status_code=404, detail="Seat not found")
    setattr(seatToUpdate, 'seat_number', seat.seat_number)
    setattr(seatToUpdate, 'screen_number', seat.screen_number)
    setattr(seatToUpdate, 'is_available', seat.is_available)
    setattr(seatToUpdate, 'theatre_id', seat.theatre_id)
    db.commit()
    db.refresh(seatToUpdate)
    return seatToUpdate

@router.delete("/deleteSeat/{seat_id}", response_model = SeatResponse)
def deleteSeat(seat_id: int, db: Session = Depends(get_db), getcurrentuser: dict = Depends(getCurrentUser)):
    if getcurrentuser['role'] not in ('admin', 'organizer'):
        raise HTTPException(status_code=403, detail="Only admin and organizer can delete seat")
    seatToDelete = db.query(models.Seat).filter(models.Seat.id == seat_id).first()
    if seatToDelete is None:
        raise HTTPException(status_code=404, detail="Seat not found")
    db.delete(seatToDelete)
    db.commit()
    return seatToDelete