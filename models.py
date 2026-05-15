from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base


class UserForm(Base):
    __tablename__ = "user_forms"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    age = Column(Integer, nullable=True)
    message = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)