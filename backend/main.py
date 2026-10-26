from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from database import get_db
from sqlalchemy import text, select
from schemas import HabitCreate, HabitResponse
from models import Habit

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Habit tracker app"}

@app.post("/habits", response_model=HabitResponse)
def create_habit(habit_data: HabitCreate, db: Session = Depends(get_db)):
    new_habit = Habit(name=habit_data.name)

    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)

    return new_habit

@app.get("/habits", response_model=list[HabitResponse])
def get_habits(db: Session = Depends(get_db)):
    statement = select(Habit)
    result = db.execute(statement)
    habits = result.scalars().all()
    return habits