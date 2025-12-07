from datetime import datetime

from sqlalchemy.orm import Session

from models import Question
from .question_schema import QuestionCreate


def get_question_list(db: Session) -> list[Question]:
    question_list = (
        db.query(Question)
        .order_by(Question.create_date.desc())
        .all()
    )
    return question_list


def get_question(db: Session, question_id: int) -> Question | None:
    question = (
        db.query(Question)
        .filter(Question.id == question_id)
        .first()
    )
    return question


def create_question(db: Session, question_create: QuestionCreate) -> Question:
    question = Question(
        subject=question_create.subject,
        content=question_create.content,
        create_date=datetime.utcnow(),
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question
