from schemas import ActivityResponse,WorkoutResponse
from sqlalchemy.orm import sessionmaker, Session, relationship


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