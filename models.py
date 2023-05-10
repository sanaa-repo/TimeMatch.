"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT
from sqlalchemy.orm import relationship
from database import Base

"User is the username, password, emial and mentor/student status of the person using the website"
class User(Base):
    __tablename__ = "users"

    # Columns
    id = Column("id", INTEGER, autoincrement = True, primary_key=True)
    username = Column("username", TEXT, nullable=False)
    password = Column("password", TEXT, nullable=False)
    email = Column("email", TEXT, nullable=False)
    usertype = Column("usertype", TEXT, nullable=False)
    # Skill update: using relationships to connect objects/tables
    availabilities = relationship("Availability", back_populates="user")
    subjects = relationship("Subject", secondary = "tutorsubjects", back_populates = "users")
    times = relationship("Time", secondary = "availabilities", back_populates = "users")

    #constructor
    def __init__(self, username, password, email, usertype):
        # id auto-increments
        self.username = username
        self.password = password
        self.email = email
        self.usertype = usertype

    def __repr__(self):
        return self.username + " is a " + self.usertype + ". Their email is" + self.email

"TutorSubject connects the User with a subject they teach/learn"
class TutorSubject(Base):
    __tablename__ = "tutorsubjects"

    #Columns
    id = Column("id", INTEGER, autoincrement = True, primary_key=True)
    subject_id = Column("subject_id", ForeignKey("subjects.id"))
    user_id = Column("user_id", ForeignKey("users.id"))

    def __init__(self, subject_id, user_id):
        # id auto-increments
        self.subject_id = subject_id
        self.user_id = user_id

"Subject has a name"
class Subject(Base):
    __tablename__ = "subjects"

    #Columns
    id = Column("id", INTEGER, autoincrement = True, primary_key=True)
    name = Column("name", TEXT, nullable = False)
    users = relationship("User", secondary = "tutorsubjects", back_populates = "subjects")
    #constructor
    def __init__(self, name):
        #id auto-increments
        self.name = name

    def __repr__(self):
        return self.name
    
"Availability connects the User with a time they are free"
class Availability(Base):
    __tablename__ = "availabilities"

    #Columns
    id = Column("id", INTEGER, autoincrement = True, primary_key=True)
    user_id = Column("user_id", ForeignKey("users.id"))
    time_id = Column("time_id", ForeignKey("times.id"))
    time = relationship("Time", back_populates= "availabilities")
    user = relationship("User", back_populates= "availabilities")
    
    #constructor
    def __init__(self, user_id, time_id):
        #id autoincrements
        self.user_id = user_id
        self.time_id = time_id

"Time that two people can meet"
class Time(Base):
    __tablename__ = "times"

    #Columns 
    id = Column("id", INTEGER, autoincrement = True, primary_key=True)
    day_of_week = Column("day_of_week", TEXT, nullable = False)
    time = Column("time", INTEGER, nullable = False)
    availabilities = relationship("Availability", back_populates="time") 
    users = relationship("User", secondary = "availabilities", back_populates = "times")


    def __init__(self, day_of_week, time):
        #id autoincrements
        self.day_of_week = day_of_week
        self.time = time

    def __repr__(self):
        return self.day_of_week + " @ " + str(self.time)




    


    
