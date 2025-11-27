# domain/question/question_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Question
from .question_schema import QuestionCreate
from . import question_crud

router = APIRouter(
    prefix='/api/question',   # 과제에서 요구한 prefix
    tags=['question'],
)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/')
def question_list(db: Session = Depends(get_db)) -> list[dict]:
    """질문 목록을 반환하는 API (GET /api/question/)."""
    questions = (
        db.query(Question)
        .order_by(Question.create_date.desc())
        .all()
    )

    result = [
        {
            'id': q.id,
            'subject': q.subject,
            'content': q.content,
            'create_date': q.create_date,
        }
        for q in questions
    ]
    return result


@router.post('/')
def create_question(
    question_create: QuestionCreate,
    db: Session = Depends(get_db),
) -> dict:
    """질문을 등록하는 API (POST /api/question/)."""
    question = question_crud.create_question(db, question_create)

    return {
        'id': question.id,
        'subject': question.subject,
        'content': question.content,
        'create_date': question.create_date,
    }
