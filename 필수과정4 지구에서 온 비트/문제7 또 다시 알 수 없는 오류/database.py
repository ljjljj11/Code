# database.py
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = 'sqlite:///./app.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


@contextmanager
def _db_context() -> Generator[Session, None, None]:
    """SessionLocal을 열고, 사용이 끝나면 자동으로 닫아주는 컨텍스트."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI 의존성으로 사용할 DB 세션.
    contextlib.contextmanager를 사용해
    매 요청마다 연결을 열고, 응답 후 닫힌다.
    """
    with _db_context() as db:
        yield db
