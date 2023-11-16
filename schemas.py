from pydantic import BaseModel, validator


class RatingCreate(BaseModel):
    value: float

    @validator("value")
    def validate_rating_value(cls, value):
        if value < 1 or value > 5:
            raise ValueError("Rating value must be between 1 and 5")
        return value
