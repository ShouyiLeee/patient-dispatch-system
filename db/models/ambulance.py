from typing import Dict, Any, Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class AmbulanceStatus(str, Enum):
    AVAILABLE = "available"
    DISPATCHED = "dispatched"
    EN_ROUTE_TO_PATIENT = "en_route_to_patient"
    WITH_PATIENT = "with_patient"
    EN_ROUTE_TO_HOSPITAL = "en_route_to_hospital"
    AT_HOSPITAL = "at_hospital"
    OUT_OF_SERVICE = "out_of_service"


class AmbulanceLocation(BaseModel):
    """Ambulance current location."""
    latitude: float
    longitude: float
    last_updated: datetime = Field(default_factory=datetime.now)


class AmbulanceCapabilities(BaseModel):
    """Specialized equipment and capabilities."""
    basic_life_support: bool = True
    advanced_life_support: bool = False
    neonatal: bool = False
    pediatric: bool = False
    mental_health: bool = False
    bariatric: bool = False
    other: List[str] = Field(default_factory=list)


class Ambulance(BaseModel):
    """Ambulance data model."""
    ambulance_id: str
    vehicle_id: str
    dispatch_id: str
    type: str  # "basic", "advanced", "specialized", etc.
    status: AmbulanceStatus = AmbulanceStatus.AVAILABLE
    location: AmbulanceLocation
    crew_count: int = 2
    capabilities: AmbulanceCapabilities = Field(default_factory=AmbulanceCapabilities)
    current_patient_id: Optional[str] = None
    current_hospital_id: Optional[str] = None
    estimated_availability: Optional[datetime] = None
    contact_number: str
    additional_info: Dict[str, Any] = Field(default_factory=dict)