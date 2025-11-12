# model.py
# -*- coding: utf-8 -*-
# PEP 8 스타일과 문자열 작은따옴표 기본 규칙을 따릅니다.

from pydantic import BaseModel, field_validator


class TodoItem(BaseModel):
    task: str

    @field_validator('task')
    @classmethod
    def validate_task(cls, value: str) -> str:
        cleaned = (value or '').strip()
        if not cleaned:
            raise ValueError('task는 비어 있을 수 없습니다.')
        return cleaned
