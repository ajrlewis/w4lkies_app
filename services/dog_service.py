import datetime
from typing import Optional

from loguru import logger
from sqlalchemy import desc

from app import db
from forms.dog_form import DogForm
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


def update_dog(dog_id: int, dog_data: dict) -> bool:
    dog = get_dog(dog_id)
    if dog:
        dog.name = dog_data.get("name")
        dog.date_of_birth = dog_data.get("date_of_birth")
        dog.breed = dog_data.get("breed")
        dog.is_allowed_treats = dog_data.get("is_allowed_treats")
        dog.is_allowed_off_the_lead = dog_data.get("is_allowed_off_the_lead")
        dog.is_allowed_on_social_media = dog_data.get("is_allowed_on_social_media")
        dog.is_neutered_or_spayed = dog_data.get("is_neutered_or_spayed")
        dog.behavioral_issues = dog_data.get("behavioral_issues")
        dog.medical_needs = dog_data.get("medical_needs")
        dog.customer_id = dog_data.get("customer_id")
        dog.vet_id = dog_data.get("vet_id")
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating {dog}: {e}")


def add_dog(dog_data: dict) -> Optional[Dog]:
    new_dog = Dog(
        name=dog_data.get("name"),
        date_of_birth=dog_data.get("date_of_birth"),
        breed=dog_data.get("breed"),
        is_allowed_treats=dog_data.get("is_allowed_treats"),
        is_allowed_off_the_lead=dog_data.get("is_allowed_off_the_lead"),
        is_allowed_on_social_media=dog_data.get("is_allowed_on_social_media"),
        is_neutered_or_spayed=dog_data.get("is_neutered_or_spayed"),
        behavioral_issues=dog_data.get("behavioral_issues"),
        medical_needs=dog_data.get("medical_needs"),
        customer_id=dog_data.get("customer_id"),
        vet_id=dog_data.get("vet_id"),
    )
    try:
        db.session.add(new_dog)
        db.session.commit()
        logger.debug(f"{new_dog = }")
        return new_dog
    except Exception as e:
        logger.error(f"Error adding dog: {e}")
        db.session.rollback()
        return


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


def get_dog_form(dog: Optional[Dog] = None) -> DogForm:
    dog_form = DogForm()
    if dog:
        dog_form.name.data = dog.name
        dog_form.date_of_birth.data = dog.date_of_birth
        dog_form.breed.data = dog.breed
        dog_form.is_allowed_treats.data = dog.is_allowed_treats
        dog_form.is_allowed_off_the_lead.data = dog.is_allowed_off_the_lead
        dog_form.is_allowed_on_social_media.data = dog.is_allowed_on_social_media
        dog_form.is_neutered_or_spayed.data = dog.is_neutered_or_spayed
        dog_form.behavioral_issues.data = dog.behavioral_issues
        dog_form.medical_needs.data = dog.medical_needs
        dog_form.customer_id.data = dog.customer_id
        dog_form.vet_id.data = dog.vet_id
    return dog_form
