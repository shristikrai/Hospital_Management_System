
from pydantic import BaseModel, Field, ConfigDict


class PatientCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    age: int = Field(ge=0, le=120)
    gender: str = Field(min_length=1, max_length=20)
    condition: str = Field(min_length=1, max_length=255)

class PatientUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    age: int | None = Field(default=None, ge=0, le=120)
    gender: str | None = Field(default=None, min_length=1, max_length=20)
    condition: str | None = Field(default=None, min_length=1, max_length=255)


class PatientResponse(PatientCreate):
    patient_id: int

    model_config = ConfigDict(from_attributes=True)
