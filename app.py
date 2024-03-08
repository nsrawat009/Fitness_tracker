from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Example database
class ExerciseDB:
    def __init__(self):
        self.exercises = []

    def add_exercise(self, exercise):
        self.exercises.append(exercise)

    def get_exercises(self):
        return self.exercises

db = ExerciseDB()

# Pydantic models
class Exercise(BaseModel):
    name: str
    sets: int
    repetitions: int

# API endpoints
@app.post("/exercise/")
def create_exercise(exercise: Exercise):
    db.add_exercise(exercise)
    return {"message": "Exercise added successfully"}

@app.get("/exercises/")
def get_exercises():
    return db.get_exercises()

# Sample data
initial_exercises = [
    {"name": "Push-ups", "sets": 3, "repetitions": 10},
    {"name": "Squats", "sets": 3, "repetitions": 15},
    {"name": "Plank", "sets": 3, "repetitions": 30}
]

for ex_data in initial_exercises:
    db.add_exercise(Exercise(**ex_data))
