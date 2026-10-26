from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class HabitCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)

class HabitResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    created_at: datetime
