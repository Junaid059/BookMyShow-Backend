from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import models
from ..db import get_db
from ..schemas.ReviewSchema import ReviewCreate, ReviewResponse
from ..auth import getCurrentUser

router = APIRouter()

@router.post("/createReview", response_model = ReviewResponse)
def createReview(review: ReviewCreate, db: Session = Depends(get_db), getcurrentuser: dict = Depends(getCurrentUser)):
    if getcurrentuser['role'] not in ('admin', 'user','organizer'):
        raise HTTPException(status_code=403, detail="YOU DONT HAVE THE PERMISSION TO CREATE REVIEW")
    newReview = models.Review(rating = review.rating, comment = review.comment, user_id = review.user_id, movie_id = review.movie_id)
    db.add(newReview)
    db.commit()
    db.refresh(newReview)
    return newReview


@router.get("/getReviews/{movie_id}", response_model = list[ReviewResponse])
def getReviews(movie_id: int, db: Session = Depends(get_db)):
    reviews = db.query(models.Review).filter(models.Review.movie_id == movie_id).all()
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found for this movie")
    return reviews

@router.put("/updateReview/{review_id}", response_model = ReviewResponse)
def updateReview(review_id: int, review: ReviewCreate, db: Session = Depends(get_db), getcurrentuser: dict = Depends(getCurrentUser)):
    existingReview = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not existingReview:
        raise HTTPException(status_code=404, detail="Review not found")
    if existingReview.user_id != getcurrentuser['id'] and getcurrentuser['role'] not in ('admin','organizer','user'):  # type: ignore[union-attr]
        raise HTTPException(status_code=403, detail="You can only update your own review or you do not have permission to update this review")
    existingReview.rating = review.rating  # type: ignore[assignment]
    existingReview.comment = review.comment  # type: ignore[assignment]
    db.commit()
    db.refresh(existingReview)
    return existingReview


@router.delete("/deleteReview?{review_id}", response_model = ReviewResponse)
def deleteReview(review_id: int, db: Session = Depends(get_db), getcurrentuser: dict = Depends(getCurrentUser)):
    existingReview = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not existingReview:
        raise HTTPException(status_code=404, detail="Review not found")
    if existingReview.user_id != getcurrentuser['id'] and getcurrentuser['role'] not in ('admin','organizer','user'):  # type: ignore[union-attr]
        raise HTTPException(status_code=403, detail="You can only delete your own review or you do not have permission to delete this review")
    db.delete(existingReview)
    db.commit()
    return existingReview