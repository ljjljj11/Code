# domain/question/question_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from .question_schema import QuestionCreate, QuestionRead
from . import question_crud

router = APIRouter(
    prefix='/api/question',
    tags=['question'],
)


@router.get('/', response_model=list[QuestionRead])
def question_list(db: Session = Depends(get_db)) -> list[QuestionRead]:
    """
    질문 목록을 반환하는 API (GET /api/question/).
    DB 세션은 get_db 의존성을 통해 요청마다 열고 닫힌다.
    """
    questions = question_crud.get_question_list(db)
    # questions는 Question ORM 객체 리스트지만,
    # QuestionRead(Config.from_attributes = True) 덕분에 자동 변환된다.
    return questions


@router.post('/', response_model=QuestionRead)
def create_question(
    question_create: QuestionCreate,
    db: Session = Depends(get_db),
) -> QuestionRead:
    """
    질문을 등록하는 API (POST /api/question/).
    """
    question = question_crud.create_question(db, question_create)
    return question
