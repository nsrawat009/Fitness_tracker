from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker


# engine=create_engine('postgresql://postgres:nathanoj35@localhost/pizza_delivery',
#     echo=True
# )
# Define database connection
SQLALCHEMY_DATABASE_URL = "sqlite:///./fitness.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Base=declarative_base()

# Session=sessionmaker()

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM
Base = declarative_base()