from sqlalchemy import Column, String, Date, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import  declarative_base
import uuid
import datetime

from sqlalchemy.orm import Session

from database import get_db

Base = declarative_base()



class Employee(Base):
    __tablename__ = 'employees'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    department = Column(String, nullable=True)
    role = Column(String, nullable=True)
    date_joined = Column(Date, default=datetime.date.today)

    __table_args__ = (
        UniqueConstraint('email', name='uq_employee_email'),
    )

class User(Base):
    __tablename__ = 'users'
    username = Column(String, primary_key=True, unique=True, nullable=False)
    password = Column(String, nullable=False)