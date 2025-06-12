from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class PatientLocation(BaseModel):
    """Patient's geographical location."""
    latitude: float
    longitude: float
    address: Optional[str] = None


class PatientSymptom(BaseModel):
    """Individual symptom with metadata."""
    name: str
    severity: Optional[float] = None  # 0-1 scale
    duration_hours: Optional[float] = None
    description: Optional[str] = None


class PatientInfo(BaseModel):
    """Basic patient information."""
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    weight_kg: Optional[float] = None
    height_cm: Optional[float] = None
    medical_history: List[str] = Field(default_factory=list)
    allergies: List[str] = Field(default_factory=list)
    medications: List[str] = Field(default_factory=list)


class Patient(BaseModel):
    """Patient data model."""
    patient_id: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    location: Optional[PatientLocation] = None
    symptoms: List[PatientSymptom] = Field(default_factory=list)
    description: Optional[str] = None
    priority: Optional[int] = None  # 1-5 scale
    specialty: Optional[str] = None
    needs_emergency: bool = False
    info: PatientInfo = Field(default_factory=PatientInfo)
    images: List[str] = Field(default_factory=list)  # Paths to images
    triage_data: Dict[str, Any] = Field(default_factory=dict)
    care_plan_id: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True