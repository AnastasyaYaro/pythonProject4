import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Берём URL из переменной окружения, а если её нет – используем SQLite
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./test.db"
)

# Для SQLite нужен параметр check_same_thread, для остальных – нет
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency‑функция для получения сессии SQLAlchemy."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()