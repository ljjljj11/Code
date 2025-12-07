# domain/question/question_frontend_router.py
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from . import question_crud
from .question_schema import QuestionCreate

router = APIRouter(
    prefix='/question',
    tags=['question-frontend'],
)

templates = Jinja2Templates(directory='frontend/templates')


@router.get('/', response_class=HTMLResponse)
def question_list_page(
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
def question_create_page(
    subject: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db),
) -> RedirectResponse:
    question_create = QuestionCreate(
        subject=subject,
        content=content,
    )
    question_crud.create_question(db, question_create)
    return RedirectResponse(url='/question/', status_code=303)
