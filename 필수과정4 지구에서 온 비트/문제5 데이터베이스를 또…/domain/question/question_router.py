from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import SessionLocal
from . import question_crud
from .question_schema import QuestionCreate

router = APIRouter(
    prefix='/question',
    tags=['question'],
)

templates = Jinja2Templates(directory='frontend/templates')


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/', response_class=HTMLResponse)
def question_list(
    request: Request,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    question_list = question_crud.get_question_list(db)
    context = {
        'request': request,
        'question_list': question_list,
    }
    return templates.TemplateResponse('question_list.html', context)


@router.get('/create', response_class=HTMLResponse)
def question_create_form(request: Request) -> HTMLResponse:
    context = {
        'request': request,
    }
    return templates.TemplateResponse('question_form.html', context)


@router.post('/create')
def question_create(
    subject: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db),
) -> RedirectResponse:
    question_create_schema = QuestionCreate(
        subject=subject,
        content=content,
    )
    question_crud.create_question(db, question_create_schema)
    return RedirectResponse(url='/question/', status_code=303)


@router.get('/{question_id}', response_class=HTMLResponse)
def question_detail(
    question_id: int,
    request: Request,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    question = question_crud.get_question(db, question_id)
    if question is None:
        return HTMLResponse(
            status_code=404,
            content='Question not found',
        )

    context = {
        'request': request,
        'question': question,
    }
    return templates.TemplateResponse('question_detail.html', context)
