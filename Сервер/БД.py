from sqlalchemy import create_engine, Column, Integer, String, Time, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import time


Base = declarative_base()


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


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False, unique=True)  
    full_name = Column(String, nullable=False)  
    password = Column(String, nullable=False)  


engine = create_engine('sqlite:///university_schedule.db')


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()


def init():
  groups = [
      Group(group_number='101'),
      Group(group_number='102'),
      Group(group_number='103')
  ]
  session.add_all(groups)
  session.commit()


  students = [
      Student(full_name=f'Студент {i}', group_id=(i % 3) + 1) 
      for i in range(1, 61)
  ]
  session.add_all(students)
  session.commit()


  instructors = [
      Instructor(full_name=f'Преподаватель {i}') 
      for i in range(1, 7)
  ]
  session.add_all(instructors)
  session.commit()


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


  users = [
      User(login=f'user{i}', full_name=f'Пользователь {i}', password=f'password{i}')
      for i in range(1, 6)
  ]
  session.add_all(users)
  session.commit()


  session.close()
if __name__=="__main__":
    init()