# Protect student routes with JWT & roles

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import StudentCreate, StudentOut, StudentUpdate
from app.services.student_service import (
    add_student_service,
    list_students_service,
    get_student_service,
    update_student_service,
    delete_student_service
)
from app.auth.security import get_current_user, require_roles
from app.models import Student

router = APIRouter(prefix="/students", tags=["Students"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Only admin can create students
@router.post("/", response_model=StudentOut)
def create_student_route(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: Student = Depends(require_roles(["admin"]))
):
    return add_student_service(db, student)


# Both admin & student can list
@router.get("/", response_model=list[StudentOut])
def list_students_route(
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_user)
):
    return list_students_service(db)


# Anyone logged in can view a specific student
@router.get("/{student_id}", response_model=StudentOut)
def get_student_route(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_user)
):
    return get_student_service(db, student_id)


# Only admin can update
@router.put("/{student_id}", response_model=StudentOut)
def update_student_route(
    student_id: int,
    student: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: Student = Depends(require_roles(["admin"]))
):
    return update_student_service(db, student_id, student)


# Only admin can delete
@router.delete("/{student_id}")
def delete_student_route(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: Student = Depends(require_roles(["admin"]))
):
    return delete_student_service(db, student_id)

