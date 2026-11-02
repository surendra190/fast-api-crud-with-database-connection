from pydantic import BaseModel, EmailStr, Field, ConfigDict

class EmployeeCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    age: int = Field(ge=18, le=65)

class EmployeeUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None = None
    age: int | None = Field(default=None, ge=18, le=65)

class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int

    model_config = ConfigDict(from_attributes=True)