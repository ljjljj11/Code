from fastapi import FastAPI, APIRouter
from typing import Dict, List
import csv
import os

app = FastAPI()
router = APIRouter()

file_path = 'todo_list.csv'
todo_list: List[Dict] = []


def save_todo(item: Dict) -> None:
    file_exists = os.path.exists(file_path)
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['task'])
        if not file_exists:
            writer.writeheader()
        writer.writerow({'task': item.get('task', '')})


def load_todo() -> List[Dict]:
    items = []
    if not os.path.exists(file_path):
        return items
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            items.append({'task': row.get('task', '')})
    return items


@router.post('/add_todo')
def add_todo(item: Dict) -> Dict:
    # 보너스 과제: 빈 Dict 경고
    if not item or 'task' not in item or not str(item['task']).strip():
        return {'warning': '입력값이 비어 있습니다. 할 일을 입력하세요.'}

    task = str(item['task']).strip()
    todo_list.append({'task': task})
    save_todo({'task': task})
    return {'message': '할 일이 추가되었습니다.', 'task': task}


@router.get('/retrieve_todo')
def retrieve_todo() -> Dict:
    todos = load_todo()
    return {'todo_list': todos}


app.include_router(router)
