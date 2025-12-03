from sqlalchemy.orm import Session
from app.crud.student_crud import (
    create_student, get_students, get_student_by_id,
    update_student, delete_student
)
from app.schemas import StudentCreate, StudentUpdate


def add_student_service(db: Session, student: StudentCreate):
    return create_student(db, student)


def list_students_service(db: Session):
    return get_students(db)


def get_student_service(db: Session, student_id: int):
    return get_student_by_id(db, student_id)


def update_student_service(db: Session, student_id: int, data: StudentUpdate):
    return update_student(db, student_id, data)


def delete_student_service(db: Session, student_id: int):
    return delete_student(db, student_id)
