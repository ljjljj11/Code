# todo.py
# -*- coding: utf-8 -*-
# FastAPI 기반, CSV 저장. 표준 라이브러리 + FastAPI만 사용합니다.

from typing import Dict, List
import csv
import os

from fastapi import FastAPI, APIRouter, HTTPException
from model import TodoItem

app = FastAPI(title='Todo API', version='1.0.0')
router = APIRouter()

FILE_PATH = 'todo_list.csv'


# ------------------------------
# CSV Utilities
# ------------------------------
def save_todo_append(task: str) -> None:
    file_exists = os.path.exists(FILE_PATH)
    with open(FILE_PATH, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['task'])
        if not file_exists:
            writer.writeheader()
        writer.writerow({'task': task})


def save_todo_overwrite(tasks: List[str]) -> None:
    with open(FILE_PATH, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['task'])
        writer.writeheader()
        for t in tasks:
            writer.writerow({'task': t})


def load_todo() -> List[Dict]:
    items: List[Dict] = []
    if not os.path.exists(FILE_PATH):
        return items
    with open(FILE_PATH, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for idx, row in enumerate(reader):
            items.append({'id': idx, 'task': row.get('task', '')})
    return items


def assert_id_in_range(todo_id: int, items: List[Dict]) -> None:
    if todo_id < 0 or todo_id >= len(items):
        raise HTTPException(status_code=404, detail='해당 ID의 할 일을 찾을 수 없습니다.')


# ------------------------------
# Endpoints
# ------------------------------
@router.post('/add_todo')
def add_todo(item: Dict) -> Dict:
    # 입력은 Dict로 받고, 필드 유효성은 모델로 재검증합니다.
    if not item or 'task' not in item:
        return {'warning': '입력값이 비어 있습니다. 할 일을 입력하세요.'}
    todo = TodoItem(task=str(item['task']))
    save_todo_append(todo.task)
    new_id = len(load_todo()) - 1
    return {'message': '할 일이 추가되었습니다.', 'id': new_id, 'task': todo.task}


@router.get('/retrieve_todo')
def retrieve_todo() -> Dict:
    todos = load_todo()
    return {'todo_list': todos}


@router.get('/todo/{todo_id}')
def get_single_todo(todo_id: int) -> Dict:
    items = load_todo()
    assert_id_in_range(todo_id, items)
    return items[todo_id]


@router.put('/todo/{todo_id}')
def update_todo(todo_id: int, payload: TodoItem) -> Dict:
    items = load_todo()
    assert_id_in_range(todo_id, items)

    tasks = [item['task'] for item in items]
    tasks[todo_id] = payload.task
    save_todo_overwrite(tasks)
    return {'message': '할 일이 수정되었습니다.', 'id': todo_id, 'task': payload.task}


@router.delete('/todo/{todo_id}')
def delete_single_todo(todo_id: int) -> Dict:
    items = load_todo()
    assert_id_in_range(todo_id, items)

    tasks = [item['task'] for item in items]
    deleted_task = tasks.pop(todo_id)
    save_todo_overwrite(tasks)
    return {'message': '할 일이 삭제되었습니다.', 'deleted': {'id': todo_id, 'task': deleted_task}}


app.include_router(router)
