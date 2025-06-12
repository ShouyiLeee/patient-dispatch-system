from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class HospitalLocation(BaseModel):
    """Hospital geographical location."""
    latitude: float
    longitude: float
    address: str


class HospitalSpecialty(BaseModel):
    """Hospital specialty with capacity."""
    name: str
    doctors_available: int = 0
    beds_total: int = 0
    beds_available: int = 0
    wait_time_minutes: Optional[int] = None


class Hospital(BaseModel):
    """Hospital data model."""
    hospital_id: str
    name: str
    type: str  # "general", "specialized", "clinic", etc.
    location: HospitalLocation
    contact_phone: str
    contact_email: Optional[str] = None
    website: Optional[str] = None
    emergency_service: bool = False
    specialties: List[HospitalSpecialty] = Field(default_factory=list)
    operating_hours: Dict[str, str] = Field(default_factory=dict)  # {"monday": "9:00-17:00", ...}
    current_load: float = 0.0  # 0.0 to 1.0
    ratings: float = 0.0  # 0.0 to 5.0
    insurance_accepted: List[str] = Field(default_factory=list)
    additional_info: Dict[str, Any] = Field(default_factory=dict)
    is_active: bool = True