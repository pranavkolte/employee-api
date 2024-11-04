from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import Query
from typing import Optional
from service.auth import Auth

from database import get_db
from database.models import User
from database.shema import EmployeeCreate, EmployeeUpdate, UserCreate, DefaultResponseModel
from fastapi.responses import ORJSONResponse

router = APIRouter()


@router.post("/", response_model=DefaultResponseModel)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        return ORJSONResponse(
            content=DefaultResponseModel(
                message=f"username: {user.username} already exist"
            ).model_dump(),
            status_code=403,
        )

    hashed_password = Auth.get_password_hash(user.password)
    new_user = User(username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return ORJSONResponse(
        content=DefaultResponseModel(
            message=f"User {user.username} created successfully",
            content={"username": new_user.username}
        ).model_dump(),
        status_code=201,
    )