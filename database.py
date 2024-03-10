from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker



SQLALCHEMY_DATABASE_URL = "sqlite:///D:/Data science/Fitness_tracker/fitness.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})



Base=declarative_base()

Session=sessionmaker()

