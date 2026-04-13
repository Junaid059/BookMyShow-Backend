from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import models
from ..db import get_db
from ..schemas.BookingSchema import BookingCreate, BookingResponse
from ..auth import getCurrentUser

router = APIRouter()

@router.post("/createBooking", response_model = BookingResponse)
def createBookng(booking: BookingCreate, db: Session = Depends(get_db), getcurrentuser: dict = Depends(getCurrentUser)):
    if getcurrentuser['role'] not in ('admin', 'user','organizer'):
        raise HTTPException(status_code=403, detail="YOU DONT HAVE THE PERMISSION TO CREATE BOOKING")
    newBooking = models.Booking(booking_date = booking.booking_date, total_amount = booking.total_amount, status = booking.status, seat_numbers = booking.seat_numbers, user_id = booking.user_id, show_id = booking.show_id)
    db.add(newBooking)
    db.commit()
    db.refresh(newBooking)
    return newBooking

@router.get("/getBookings", response_model = list[BookingResponse])
def getBookings(db: Session = Depends(get_db), getcurrentuser : dict = Depends(getCurrentUser)):
    if getcurrentuser['role'] in ('admin', 'organizer'):
        bookings = db.query(models.Booking).all()
    else:
        bookings = db.query(models.Booking).filter(models.Booking.user_id == getcurrentuser['id']).all()
    if not bookings:
        raise HTTPException(status_code=404, detail="No bookings found")
    return bookings

@router.get("/getBookingbyId/{booking_id}", response_model = BookingResponse)
def getBookingbyId(booking_id: int, user_id: int, db: Session = Depends(get_db), getcurrentuser : dict = Depends(getCurrentUser)):
    if getcurrentuser['role'] not in ('admin', 'organizer', 'user') or getcurrentuser['id'] != user_id:
        raise HTTPException(status_code=403, detail="You do not have permission to view this booking")
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id, models.Booking.user_id == user_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.put("/updateBooking/{booking_id}", response_model = BookingResponse)
def updateBooking(booking_id: int, user_id: int, booking: BookingResponse, db: Session = Depends(get_db), getcurrentuser : dict =  Depends(getCurrentUser)):
    if getcurrentuser['role'] not in ('admin', 'organizer') or getcurrentuser['id'] != user_id:
        raise HTTPException(status_code=403, detail="You do not have permission to update this booking")
    existingBooking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not existingBooking:
        raise HTTPException(status_code=404, detail="Booking not found")
    setattr(existingBooking, 'booking_date', booking.booking_date)
    setattr(existingBooking, 'total_amount', booking.total_amount)
    setattr(existingBooking, 'status', booking.status)
    setattr(existingBooking, 'seat_numbers', booking.seat_numbers)
    setattr(existingBooking, 'user_id', booking.user_id)
    setattr(existingBooking, 'show_id', booking.show_id)
    db.commit()
    db.refresh(existingBooking)
    return existingBooking

@router.delete("/deleteBooking/{booking_id}", response_model = BookingResponse)
def deleteBooking(booking_id: int, user_id: int, db: Session = Depends(get_db), getcurrentuser : dict = Depends(getCurrentUser)):
    if getcurrentuser['role'] not in ('admin', 'organizer', 'user') or getcurrentuser['id'] != user_id:
        raise HTTPException(status_code=403, detail="You do not have permission to delete this booking")
    existingBooking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not existingBooking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(existingBooking)
    db.commit()
    return existingBooking
