# client.py
# -*- coding: utf-8 -*-
# 표준 라이브러리만 사용하여 FastAPI 서버를 호출하는 간단한 CLI 클라이언트입니다.
# PEP 8과 작은따옴표 기본 규칙을 따릅니다.

import json
import sys
from typing import Any, Dict, Optional, List
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

BASE_URL = 'http://127.0.0.1:8000'


def _request(method: str, path: str, body: Optional[Dict[str, Any]] = None) -> None:
    url = f'{BASE_URL}{path}'
    data = None
    headers = {'Accept': 'application/json'}
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode('utf-8')
        headers['Content-Type'] = 'application/json; charset=utf-8'

    req = Request(url=url, data=data, method=method, headers=headers)
    try:
        with urlopen(req) as resp:
            payload = resp.read().decode('utf-8')
            print(f'[HTTP {resp.status}] {url}')
            if payload:
                try:
                    parsed = json.loads(payload)
                    print(json.dumps(parsed, ensure_ascii=False, indent=2))
                except json.JSONDecodeError:
                    print(payload)
    except HTTPError as exc:
        print(f'[HTTP {exc.code}] {url}')
        detail = exc.read().decode('utf-8')
        try:
            parsed = json.loads(detail)
            print(json.dumps(parsed, ensure_ascii=False, indent=2))
        except json.JSONDecodeError:
            print(detail)
    except URLError as exc:
        print(f'[ERROR] 서버에 연결할 수 없습니다: {exc.reason}')


def add_todo_cli(task: str) -> None:
    _request('POST', '/add_todo', {'task': task})


def retrieve_todo_cli() -> None:
    _request('GET', '/retrieve_todo')


def get_single_todo_cli(todo_id: int) -> None:
    _request('GET', f'/todo/{todo_id}')


def update_todo_cli(todo_id: int, task: str) -> None:
    _request('PUT', f'/todo/{todo_id}', {'task': task})


def delete_single_todo_cli(todo_id: int) -> None:
    _request('DELETE', f'/todo/{todo_id}')


def print_help() -> None:
    print('''사용법:
  python client.py add "<task>"
  python client.py list
  python client.py get <id>
  python client.py update <id> "<task>"
  python client.py delete <id>

예시:
  python client.py add "화성 일지 정리"
  python client.py list
  python client.py get 0
  python client.py update 0 "화성 일지 정리 - 보강"
  python client.py delete 0
''')


def main(argv: List[str]) -> None:
    if len(argv) < 2:
        print_help()
        return

    cmd = argv[1]
    if cmd == 'add' and len(argv) >= 3:
        add_todo_cli(argv[2])
    elif cmd == 'list':
        retrieve_todo_cli()
    elif cmd == 'get' and len(argv) >= 3 and argv[2].isdigit():
        get_single_todo_cli(int(argv[2]))
    elif cmd == 'update' and len(argv) >= 4 and argv[2].isdigit():
        update_todo_cli(int(argv[2]), argv[3])
    elif cmd == 'delete' and len(argv) >= 3 and argv[2].isdigit():
        delete_single_todo_cli(int(argv[2]))
    else:
        print_help()


if __name__ == '__main__':
    main(sys.argv)
