from datetime import datetime

from pydantic import BaseModel


class QuestionCreate(BaseModel):
    subject: str
    content: str


class QuestionRead(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime

    class Config:
        from_attributes = True
