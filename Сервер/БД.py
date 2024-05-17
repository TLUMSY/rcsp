from sqlalchemy import create_engine, Column, Integer, String, Time, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import time
from fastapi import FastAPI, HTTPException, Depends

Base = declarative_base()

# Ассоциативная таблица для связи многие-ко-многим между студентами и расписанием занятий
student_class_association = Table('student_class', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('class_schedule_id', Integer, ForeignKey('class_schedules.id'))
)

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    group_number = Column(String, nullable=False) 
    students = relationship('Student', back_populates='group')  
    class_schedules = relationship('ClassSchedule', back_populates='group')  

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)  
    group_id = Column(Integer, ForeignKey('groups.id')) 
    group = relationship('Group', back_populates='students')  
    class_schedules = relationship('ClassSchedule', secondary=student_class_association, back_populates='students')

class Instructor(Base):
    __tablename__ = 'instructors'
    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False) 
    class_schedules = relationship('ClassSchedule', back_populates='instructor')  

class ClassSchedule(Base):
    __tablename__ = 'class_schedules'
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id'))  
    subject_name = Column(String, nullable=False)  
    class_time = Column(Time, nullable=False) 
    instructor_id = Column(Integer, ForeignKey('instructors.id'))  
    group = relationship('Group', back_populates='class_schedules')  
    instructor = relationship('Instructor', back_populates='class_schedules')  
    students = relationship('Student', secondary=student_class_association, back_populates='class_schedules')

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False, unique=True)  
    full_name = Column(String, nullable=False)  
    password = Column(String, nullable=False)  

# Создание базы данных
engine = create_engine('postgresql+psycopg2://postgres:123456@185.195.25.237:5431/rksp')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def init():
    # Добавление групп
    groups = [
        Group(group_number='101'),
        Group(group_number='102'),
        Group(group_number='103')
    ]
    session.add_all(groups)
    session.commit()

    # Добавление студентов
    students = [
        Student(full_name=f'Студент {i}', group_id=(i % 3) + 1) 
        for i in range(1, 61)
    ]
    session.add_all(students)
    session.commit()

    # Добавление преподавателей
    instructors = [
        Instructor(full_name=f'Преподаватель {i}') 
        for i in range(1, 7)
    ]
    session.add_all(instructors)
    session.commit()

    # Добавление расписания
    class_schedules = [
        ClassSchedule(group_id=1, subject_name='Математика', class_time=time(9, 0), instructor_id=1),
        ClassSchedule(group_id=2, subject_name='Программирование', class_time=time(10, 30), instructor_id=2),
        ClassSchedule(group_id=3, subject_name='Физика', class_time=time(12, 0), instructor_id=3),
        ClassSchedule(group_id=1, subject_name='Химия', class_time=time(13, 30), instructor_id=4),
        ClassSchedule(group_id=2, subject_name='Инженерная графика', class_time=time(15, 0), instructor_id=5),
        ClassSchedule(group_id=3, subject_name='Механика', class_time=time(16, 30), instructor_id=6)
    ]
    session.add_all(class_schedules)
    session.commit()

    # Присвоение студентов к занятиям
    for student in students:
        student.class_schedules.append(class_schedules[student.id % 6])
    session.commit()

    # Добавление пользователей
    users = [
        User(login=f'user{i}', full_name=f'Пользователь {i}', password=f'password{i}')
        for i in range(1, 6)
    ]
    session.add_all(users)
    session.commit()

    session.close()

def get_student_schedule(user_id: int):
    session = Session()
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    student = session.query(Student).filter(Student.full_name == user.full_name).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    schedule = []
    for class_schedule in student.class_schedules:
        schedule.append({
            "subject_name": class_schedule.subject_name,
            "class_time": class_schedule.class_time,
            "instructor": class_schedule.instructor.full_name
        })
    session.close()
    return schedule

def get_instructor_schedule(instructor_id: int):
    session = Session()
    instructor = session.query(Instructor).filter(Instructor.id == instructor_id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")

    schedule = []
    for class_schedule in instructor.class_schedules:
        schedule.append({
            "subject_name": class_schedule.subject_name,
            "class_time": class_schedule.class_time,
            "group_number": class_schedule.group.group_number
        })
    session.close()
    return schedule

def get_group_students(group_id: int):
    session = Session()
    group = session.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    students = []
    for student in group.students:
        students.append({
            "student_id": student.id,
            "full_name": student.full_name
        })
    session.close()
    return students