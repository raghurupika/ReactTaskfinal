from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.schemas import UserCreate, UserOut, Token, LoginSchema
from app.models import Student
from app.auth.security import (
    get_password_hash,
    verify_password,
    create_access_token,
)
from app.database import get_db
from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut, status_code=201)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # Check if username already exists
    existing_user = db.query(Student).filter(Student.username == user_in.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    existing_email = db.query(Student).filter(Student.email == user_in.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password safely (truncate if too long)
    hashed_pw = get_password_hash(user_in.password)

    # Create user and include email!
    new_user = Student(
        username=user_in.username,
        password=hashed_pw,  # store hashed password in the `password` column
        role=user_in.role,
        email=user_in.email
    )


    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ---------------- LOGIN -----------------
@router.post("/login", response_model=Token)
def login_user(user_in: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(Student).filter(Student.username == user_in.username).first()

    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username, "role": user.role},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
