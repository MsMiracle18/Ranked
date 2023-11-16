from sqlalchemy.orm import Session
from ..models import Rating

def create_rating(db: Session, photo_id: int, user_id: int, value: int):
    rating = Rating(value=value, photo_id=photo_id, user_id=user_id)
    db.add(rating)
    db.commit()
    db.refresh(rating)
    return rating

def get_average_rating(db: Session, photo_id: int):
    result = db.query(func.avg(Rating.value).label('average_rating')).filter(Rating.photo_id == photo_id).first()
    return result[0] if result[0] else 0.0

