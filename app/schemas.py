from pydantic import BaseModel, Field

class UserInput(BaseModel):
    user_id: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(gt=0, lt=120)
    weight: str = Field(min_length=1, max_length=50)
    goal: str = Field(min_length=1, max_length=100)
    intensity: str = Field(min_length=1, max_length=50)
