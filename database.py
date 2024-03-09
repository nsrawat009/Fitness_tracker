from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker


# engine=create_engine('postgresql://postgres:nathanoj35@localhost/pizza_delivery',
#     echo=True
# )
# Define database connection
# SQLALCHEMY_DATABASE_URL = "sqlite:///./fitness.db"
SQLALCHEMY_DATABASE_URL = "sqlite:///C:/Users/NH2854/Downloads/DB.Browser.for.SQLite-3.12.2-win64/DB Browser for SQLite/fitness.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Base=declarative_base()

# Session=sessionmaker()

Base=declarative_base()

Session=sessionmaker()

