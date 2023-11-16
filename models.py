from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer)
    photo_id = Column(Integer, ForeignKey("photos.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)

    ratings = relationship("Rating", back_populates="photo")
