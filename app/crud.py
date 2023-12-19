from sqlalchemy.orm import Session

from . import models, schemas


def get_question(db: Session, question_id: int):
    return db.query(models.Question).filter(models.Question.id == question_id).first()


def get_solution(db: Session, solution_id: int):
    return db.query(models.Solution).filter(models.Solution.id == solution_id).first()


def get_attempt(db: Session, attempt_id: int):
    return db.query(models.Attempt).filter(models.Attempt.id == attempt_id).first()


def create_attempt(db: Session, attempt: schemas.AttemptCreate):
    db_attempt = models.Attempt(**attempt.dict())
    db.add(db_attempt)
    db.commit()
    db.refresh(db_attempt)
    return db_attempt
