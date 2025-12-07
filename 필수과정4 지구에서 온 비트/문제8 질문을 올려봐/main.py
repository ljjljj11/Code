# main.py
from fastapi import FastAPI

from domain.question import router as question_api_router
from domain.question.question_frontend_router import router as question_frontend_router

app = FastAPI()

# JSON API
app.include_router(question_api_router)

# HTML 프론트엔드
app.include_router(question_frontend_router)