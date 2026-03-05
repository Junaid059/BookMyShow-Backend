from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    bookings = relationship("Booking", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    notifications = relationship("Notification", back_populates="user")

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)  # in minutes
    release_date = Column(DateTime, nullable=False)
    genre = Column(String, nullable=False)
    rating = Column(String, nullable=False) 
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    shows = relationship("Show", back_populates="movie")
    reviews = relationship("Review", back_populates="movie")

class Theatre(Base):
    __tablename__ = 'theatres'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    total_screens = Column(Integer, nullable=False)
    
    shows = relationship("Show", back_populates="theatre")
    city = relationship("City", back_populates="theatres")
    seats = relationship("Seat", back_populates="theatre")

class Show(Base):
    __tablename__ = 'shows'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    show_time = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    screen_number = Column(Integer, nullable=False)
    
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    theatre_id = Column(Integer, ForeignKey('theatres.id'), nullable=False)
    
    movie = relationship("Movie", back_populates="shows")
    theatre = relationship("Theatre", back_populates="shows")
    bookings = relationship("Booking", back_populates="show")

class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    booking_date = Column(DateTime, default=datetime.datetime.utcnow)
    total_amount = Column(Float, nullable=False)
    status = Column(String, nullable=False, default='confirmed')
    seat_numbers = Column(String, nullable=False) 
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    show_id = Column(Integer, ForeignKey('shows.id'), nullable=False)
    
    user = relationship("User", back_populates="bookings")
    show = relationship("Show", back_populates="bookings")
    payment = relationship("Payment", back_populates="booking")

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    comment = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    
    user = relationship("User", back_populates="reviews")
    movie = relationship("Movie", back_populates="reviews")

class Seat(Base):
    __tablename__ = 'seats'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    seat_number = Column(String, nullable=False)
    screen_number = Column(Integer, nullable=False)
    is_available = Column(Integer, nullable=False, default=1)
    theatre_id = Column(Integer, ForeignKey('theatres.id'), nullable=False)
    theatre = relationship("Theatre", back_populates="seats")

class Payment(Base):
    __tablename__ = 'payments'
    id= Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, default=datetime.datetime.utcnow)
    payment_method = Column(String, nullable=False)
    status = Column(String, nullable=False, default='pending')
    booking_id = Column(Integer, ForeignKey('bookings.id'), nullable=False)
    booking = relationship("Booking", back_populates="payment")


class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    state = Column(String, nullable=False)
    
    theatres = relationship("Theatre", back_populates="city")


class Notification(Base):
    __tablename__= 'notifications'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    message = Column(String,nullable = False)
    notification_type  = Column(String, nullable=False)
    is_read = Column(Integer,nullable = False,default = 0)
    created_at = Column(DateTime,default = datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="notifications")
