from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database.connect import get_db
from ..repository import ratings as repository_ratings
from ..models import User
from ..services.auth import auth_service

router = APIRouter(tags=["ratings"])

@router.post("/{photo_id}", response_model=Rating)
def rate_photo(photo_id: int,
               value: int,
               db: Session = Depends(get_db),
               current_user: User = Depends(auth_service.get_current_user)
               ):
    # Перевірка, чи користувач оцінює чуже фото
    photo = repository_photos.get_photo(db, photo_id)
    if not photo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")

    if photo.user_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot rate your own photo")

    # Перевірка, чи користувач вже оцінював це фото
    existing_rating = repository_ratings.get_rating_by_user(db, photo_id, current_user.id)
    if existing_rating:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already rated this photo")

    # Оцінювання фото
    new_rating = repository_ratings.create_rating(db, photo_id, current_user.id, value)
    
    # Оновлення середнього рейтингу фото
    average_rating = repository_ratings.get_average_rating(db, photo_id)
    photo.average_rating = average_rating
    db.commit()
    db.refresh(photo)

    return new_rating

@router.get("/{photo_id}/average", response_model=float)
def get_average_rating(photo_id: int, db: Session = Depends(get_db)):
    return repository_ratings.get_average_rating(db, photo_id)
