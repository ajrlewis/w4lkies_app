import datetime
from typing import Optional

from loguru import logger
from sqlalchemy import desc

from app import db
from models.dog import Dog


def get_dogs() -> list[Dog]:
    dogs = db.session.query(Dog).order_by(Dog.name).all()
    logger.debug(f"{dogs = }")
    return dogs


def get_dog(dog_id: int) -> Optional[Dog]:
    dog = db.session.get(Dog, dog_id)
    logger.debug(f"{dog = }")
    return dog


def get_dog_breeds() -> list[str]:
    results = db.session.query(Dog.breed).filter(Dog.breed.isnot(None)).distinct().all()
    dog_breeds = [result[0] for result in results]
    logger.debug(f"{dog_breeds = }")
    return dog_breeds


def delete_dog(dog_id: int) -> bool:
    dog = get_dog(dog_id)
    if dog:
        db.session.delete(dog)
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting {dog}: {e}")
            return False
    return False
