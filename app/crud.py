from sqlalchemy.orm import Session

from . import models, schemas


def get_attempt(db: Session, attempt_id: str):
    return db.query(models.Attempt).filter(models.Attempt.id == attempt_id).first()


def create_attempt(db: Session, attempt: schemas.Attempt):
    db_attempt = models.Attempt(**attempt.dict())
    db.add(db_attempt)
    db.commit()
    db.refresh(db_attempt)
    return db_attempt
