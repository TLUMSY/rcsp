from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List, Optional
import time
from БД import *
Base = declarative_base()
engine = create_engine('sqlite:///university_schedule.db')
Session = sessionmaker(bind=engine)

def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()


class GroupBase(BaseModel):
    group_number: str

class GroupCreate(GroupBase):
    pass

class GroupRead(GroupBase):
    id: int

    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    full_name: str
    group_id: int

class StudentCreate(StudentBase):
    pass

class StudentRead(StudentBase):
    id: int

    class Config:
        from_attributes = True

class InstructorBase(BaseModel):
    full_name: str

class InstructorCreate(InstructorBase):
    pass

class InstructorRead(InstructorBase):
    id: int

    class Config:
        from_attributes = True

class ClassScheduleBase(BaseModel):
    group_id: int
    subject_name: str
    class_time: time
    instructor_id: int

class ClassScheduleCreate(ClassScheduleBase):
    pass

class ClassScheduleRead(ClassScheduleBase):
    id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    login: str
    full_name: str
    password: str

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True


app = FastAPI()

@app.get('/groups', response_model=List[GroupRead])
def get_groups(session: Session = Depends(get_session)):
    return session.query(Group).all()

@app.get('/groups/{group_id}', response_model=GroupRead)
def get_group(group_id: int, session: Session = Depends(get_session)):
    group = session.query(Group).get(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

@app.post('/groups', response_model=GroupRead)
def create_group(group: GroupCreate, session: Session = Depends(get_session)):
    new_group = Group(**group.dict())
    session.add(new_group)
    session.commit()
    session.refresh(new_group)
    return new_group

@app.put('/groups/{group_id}', response_model=GroupRead)
def update_group(group_id: int, group_update: GroupCreate, session: Session = Depends(get_session)):
    group = session.query(Group).get(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    for key, value in group_update.dict().items():
        setattr(group, key, value)
    session.commit()
    session.refresh(group)
    return group

@app.delete('/groups/{group_id}')
def delete_group(group_id: int, session: Session = Depends(get_session)):
    group = session.query(Group).get(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    session.delete(group)
    session.commit()
    return {"message": "Group deleted"}


@app.get('/students', response_model=List[StudentRead])
def get_students(session: Session = Depends(get_session)):
    return session.query(Student).all()

@app.get('/students/{student_id}', response_model=StudentRead)
def get_student(student_id: int, session: Session = Depends(get_session)):
    student = session.query(Student).get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.post('/students', response_model=StudentRead)
def create_student(student: StudentCreate, session: Session = Depends(get_session)):
    new_student = Student(**student.dict())
    session.add(new_student)
    session.commit()
    session.refresh(new_student)
    return new_student

@app.put('/students/{student_id}', response_model=StudentRead)
def update_student(student_id: int, student_update: StudentCreate, session: Session = Depends(get_session)):
    student = session.query(Student).get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    for key, value in student_update.dict().items():
        setattr(student, key, value)
    session.commit()
    session.refresh(student)
    return student

@app.delete('/students/{student_id}')
def delete_student(student_id: int, session: Session = Depends(get_session)):
    student = session.query(Student).get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    session.delete(student)
    session.commit()
    return {"message": "Student deleted"}

@app.get('/instructors', response_model=List[InstructorRead])
def get_instructors(session: Session = Depends(get_session)):
    return session.query(Instructor).all()

@app.get('/instructors/{instructor_id}', response_model=InstructorRead)
def get_instructor(instructor_id: int, session: Session = Depends(get_session)):
    instructor = session.query(Instructor).get(instructor_id)
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return instructor

@app.post('/instructors', response_model=InstructorRead)
def create_instructor(instructor: InstructorCreate, session: Session = Depends(get_session)):
    new_instructor = Instructor(**instructor.dict())
    session.add(new_instructor)
    session.commit()
    session.refresh(new_instructor)
    return new_instructor

@app.put('/instructors/{instructor_id}', response_model=InstructorRead)
def update_instructor(instructor_id: int, instructor_update: InstructorCreate, session: Session = Depends(get_session)):
    instructor = session.query(Instructor).get(instructor_id)
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    for key, value in instructor_update.dict().items():
        setattr(instructor, key, value)
    session.commit()
    session.refresh(instructor)
    return instructor

@app.delete('/instructors/{instructor_id}')
def delete_instructor(instructor_id: int, session: Session = Depends(get_session)):
    instructor = session.query(Instructor).get(instructor_id)
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    session.delete(instructor)
    session.commit()
    return {"message": "Instructor deleted"}



