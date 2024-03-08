from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from typing import List, Optional
from datetime import datetime
from fastapi.responses import JSONResponse
import numpy as np
import matplotlib.pyplot as plt

# Define database connection
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM
Base = declarative_base()

# Define models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)

    activities = relationship("Activity", back_populates="owner")
    workouts = relationship("Workout", back_populates="owner")

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="activities")

class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True)
    duration = Column(Integer, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="workouts")

# Define FastAPI instance
app = FastAPI(
    title="Fitness Tracker API",
    description="API for tracking and managing fitness activities, workouts, and progress.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Secret key for JWT token
import os

SECRET_KEY = os.getenv("SECRET_KEY", "secret")

# Algorithm used for JWT
ALGORITHM = "HS256"

# Define password context for password hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define OAuth2 scheme for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# User model
class UserOut(BaseModel):
    id: int
    username: str
    email: str
    disabled: Optional[bool] = None

    class Config:
        orm_mode = True

# Token model
class Token(BaseModel):
    access_token: str
    token_type: str

# User credentials model
class UserInDB(BaseModel):
    username: str
    email: str
    hashed_password: str
    disabled: Optional[bool] = None

    class Config:
        orm_mode = True

# Get user from database
def get_user(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()

# Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Authenticate user
async def authenticate_user(email: str, password: str, db: Session):
    user = get_user(email, db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Create access token
def create_access_token(data: dict):
    to_encode = data.copy()
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get current user
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(email, db)
    if user is None:
        raise credentials_exception
    return user


# Health check endpoint
# @app.get("/")
# async def read_root():
#     return {"Hello": "World"}

# Login endpoint
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# Pydantic model for Activity
class ActivityResponse(BaseModel):
    id: int
    name: str
    description: str
    user_id: int

    class Config:
        orm_mode = True  # This tells Pydantic to use ORM mode for this model

# Pydantic model for Workout
class WorkoutResponse(BaseModel):
    id: int
    date: str
    duration: int
    user_id: int

    class Config:
        orm_mode = True  # This tells Pydantic to use ORM mode for this model

from pydantic import BaseModel

class ActivityCreate(BaseModel):
    name: str
    description: str
    user_id: int

class ActivityUpdate(BaseModel):
    name: str
    description: str

class WorkoutCreate(BaseModel):
    duration: int
    user_id: int

class WorkoutUpdate(BaseModel):
    duration: int


# Create new activity endpoint
@app.post("/activities/", response_model=ActivityResponse)
def create_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
    new_activity = Activity(**activity.dict())
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    return new_activity

# Retrieve all activities endpoint
@app.get("/activities/", response_model=List[ActivityResponse])
def get_activities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Activity).offset(skip).limit(limit).all()

# Retrieve activity by ID endpoint
@app.get("/activities/{activity_id}", response_model=ActivityResponse)
def get_activity(activity_id: int, db: Session = Depends(get_db)):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
    return activity

# Update activity endpoint
@app.put("/activities/{activity_id}", response_model=ActivityResponse)
def update_activity(activity_id: int, activity_data: ActivityUpdate, db: Session = Depends(get_db)):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
    for key, value in activity_data.dict().items():
        setattr(activity, key, value)
    db.commit()
    db.refresh(activity)
    return activity

# Delete activity endpoint
@app.delete("/activities/{activity_id}")
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
    db.delete(activity)
    db.commit()
    return



# Calculate workout summary endpoint
@app.get("/workout-summary/", response_class=JSONResponse)
def get_workout_summary(db: Session = Depends(get_db)):
    workouts = db.query(Workout).all()
    durations = [workout.duration for workout in workouts]
    total_workouts = len(workouts)
    total_duration = sum(durations)
    average_duration = np.mean(durations)
    max_duration = max(durations)
    min_duration = min(durations)

    summary_data = {
        "total_workouts": total_workouts,
        "total_duration": total_duration,
        "average_duration": average_duration,
        "max_duration": max_duration,
        "min_duration": min_duration
    }
    return summary_data

# Generate progress chart endpoint
@app.get("/progress-chart/")
def generate_progress_chart(db: Session = Depends(get_db)):
    workouts = db.query(Workout).all()
    dates = [datetime.strptime(workout.date, "%Y-%m-%d") for workout in workouts]
    durations = [workout.duration for workout in workouts]

    plt.plot(dates, durations)
    plt.xlabel('Date')
    plt.ylabel('Duration (minutes)')
    plt.title('Workout Progress Chart')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # Save the plot as a PNG image
    plt.savefig('progress_chart.png')

    # Return the path to the generated image
    return FileResponse("progress_chart.png")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(main, host="127.0.0.1", port=8000)