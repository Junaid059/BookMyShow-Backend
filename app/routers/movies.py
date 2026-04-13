from fastapi import HTTPException, status, Depends,APIRouter
from sqlalchemy.orm import Session
from ..schemas.movieSchema import MovieCreate, MovieResponse,MovieUpdate, MovieDelete
from ..models import models
from ..db import get_db
from ..auth import getCurrentUser

router = APIRouter()

@router.post("/createMovie", response_model = MovieResponse)
def createMovie(movie: MovieCreate, db: Session = Depends(get_db),getcurrentuser: dict =Depends(getCurrentUser)):
    if getcurrentuser['role'] not in ('admin', 'organizer'):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Only admins and editors can access this resource")
    newMovie = db.query(models.Movie).filter(models.Movie.title == movie.title).first()
    if newMovie:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Movie already exists")
    newMovie = models.Movie(title = movie.title, description = movie.description, duration = movie.duration, release_date = movie.release_date, genre = movie.genre, rating = movie.rating)
    db.add(newMovie)
    db.commit()
    db.refresh(newMovie)
    return newMovie

@router.get("/getMovies", response_model=list[MovieResponse])
def getMovies(db: Session = Depends(get_db)):
    movies = db.query(models.Movie).all()
    return movies

@router.get("/getMovie/{movie_id}",response_model = MovieResponse)
def getMovie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Movie not found")
    return movie

@router.put("/updateMovie/{movie_id}",response_model = MovieResponse)
def updateMovie(movie_id: int, movie: MovieUpdate, db: Session = Depends(get_db), getcurrentuser : dict = Depends(getCurrentUser)):
    if getcurrentuser['role'] not in ('admin', 'organizer'):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Only admins and organizers can access this resource")
    updatedMovie =  db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not updatedMovie:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Movie not found")
    setattr(updatedMovie,"title",movie.title)
    setattr(updatedMovie,"description",movie.description)
    setattr(updatedMovie,"duration",movie.duration)
    setattr(updatedMovie,"release_date",movie.release_date)
    setattr(updatedMovie,"genre",movie.genre)
    setattr(updatedMovie,"rating",movie.rating)
    db.commit()
    db.refresh(updatedMovie)
    return updatedMovie

@router.delete("/deleteMovie/{movie_id}",response_model = MovieDelete)
def deleteMovie(movie_id: int, d: Session = Depends(get_db), getcurrentuser : dict = Depends(getCurrentUser)):
    if getcurrentuser['role'] not in ('admin', 'organizer'):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Only admins and organizers can access this resource")
    movie_to_delete = d.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie_to_delete:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Movie not found")
    d.delete(movie_to_delete)
    d.commit()
    return movie_to_delete
