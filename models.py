from sqlalchemy import Float, DateTime
from sqlalchemy_utils import ChoiceType
from database import Base
from sqlalchemy import Column, Integer, Boolean, Text, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__='user'
    id=Column(Integer,primary_key=True)
    username=Column(String(25),unique=True)
    email=Column(String(80),unique=True)
    password=Column(Text,nullable=True)
    is_admin=Column(Boolean,default=False)
    is_active=Column(Boolean,default=False)
    exercises=relationship('Exercise',back_populates='user')


    def __repr__(self):
        return f"<User {self.username}>"

class Exercise(Base):


    EXERCISES_TYPES=(
            ('PUSHUPS','pushups'),
            ('Squats','squats'),
            ('Plank','plank'),
        )



    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    exercise_name = Column(ChoiceType(choices=EXERCISES_TYPES),default="PUSHUPS")
    sets = Column(Integer,nullable=False)
    repetitions = Column(Integer,nullable=False)
    weight_lifted = Column(Float, index=True)
    distance_covered = Column(Float, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    calories_burned = Column(Float, index=True)
    intensity_level = Column(ChoiceType([("low", "Low"), ("medium", "Medium"), ("high", "High")]), index=True)  
    performance_notes = Column(Text)
    user_id=Column(Integer,ForeignKey('user.id'))
    user = relationship("User", back_populates="exercises")

    def __repr__(self):
        return f"<Exercise {self.id}>"
