from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from domain.question import router as question_router

app = FastAPI()

# 라우터 등록
app.include_router(question_router)

# (필요하다면) 정적 파일 사용 예시
# app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
