# CRUD — student_crud.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Student
from app.schemas import StudentCreate, StudentUpdate

def create_student(db: Session, student: StudentCreate):
    db_obj = Student(name=student.name, email=student.email)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_students(db: Session):
    return db.query(Student).all()



def get_student_by_id(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


def update_student(db: Session, student_id: int, student_data: StudentUpdate):
    student = get_student_by_id(db, student_id)

    if student_data.name is not None:
        student.name = student_data.name

    if student_data.email is not None:
        student.email = student_data.email

    db.commit()
    db.refresh(student)
    return student


def delete_student(db: Session, student_id: int):
    student = get_student_by_id(db, student_id)

    db.delete(student)
    db.commit()

    return {"message": f"Student {student_id} deleted successfully"}