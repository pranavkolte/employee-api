from datetime import timedelta

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from database.models import User
from routes.empolyee import router as employee_router
from routes.user import router as user_router
from service.auth import Auth

app = FastAPI(
    debug=True,
    title="employee-api",
    contact={
        "name": "Pranav Kolte",
        "email": "pranavkolte111@gmail.com",
    },
    docs_url="/docs",
    version="0.1.0"
)

@app.get("/", tags=["Health Check"])
async def index():
    return {"message": "server is running"}


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not Auth.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=Auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = Auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

app.include_router(prefix="/api/employee", router=employee_router, tags=["Employee"])
app.include_router(prefix="/api/user", router=user_router, tags=["User"])
