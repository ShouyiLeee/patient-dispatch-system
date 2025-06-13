"""
Ambulance Dispatcher Module for Patient Care System
Handles ambulance dispatch and coordination
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
import random
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class AmbulanceDispatcher:
    """Manages ambulance dispatch operations"""
    
    def __init__(self, database_path: Optional[str] = None):
        """
        Initialize the ambulance dispatcher
        
        Args:
            database_path: Path to the ambulance database JSON file
        """
        self.database_path = database_path or os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "data", "dispatch_db.json"
        )
        self.ambulances = self._load_ambulances()
    
    def _load_ambulances(self) -> List[Dict[str, Any]]:
        """Load ambulance data from database"""
        try:
            if os.path.exists(self.database_path):
                with open(self.database_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return data.get("ambulances", [])
            else:
                logger.warning(f"Database not found at {self.database_path}, using mock data")
                return self._generate_mock_ambulances()
        except Exception as e:
            logger.error(f"Error loading ambulance data: {e}")
            return self._generate_mock_ambulances()
    
    def _generate_mock_ambulances(self) -> List[Dict[str, Any]]:
        """Generate mock ambulance data for testing"""
        ambulance_types = ["Cấp cứu", "Vận chuyển thường", "Cấp cứu nâng cao", "Hồi sức"]
        statuses = ["Sẵn sàng", "Đang di chuyển", "Đang vận chuyển bệnh nhân"]
        
        mock_ambulances = []
        for i in range(1, 11):
            ambulance_id = f"AMB{i:03d}"
            ambulance_type = random.choice(ambulance_types)
            
            # Randomly assign locations around Ho Chi Minh City center
            lat_base, lng_base = 10.7756587, 106.7004238  # HCMC center
            lat = lat_base + (random.random() - 0.5) * 0.05
            lng = lng_base + (random.random() - 0.5) * 0.05
            
            mock_ambulances.append({
                "id": ambulance_id,
                "type": ambulance_type,
                "status": random.choice(statuses) if i > 5 else "Sẵn sàng",
                "location": {
                    "latitude": lat,
                    "longitude": lng,
                    "address": f"Địa điểm {i}, Quận {random.randint(1, 12)}, TP. HCM"
                },
                "staff": {
                    "driver": f"Tài xế {i}",
                    "medics": [f"Nhân viên y tế {i}A", f"Nhân viên y tế {i}B"]
                },
                "equipment": {
                    "basic": True,
                    "advanced": i % 3 == 0,
                    "ventilator": i % 5 == 0
                }
            })
        
        return mock_ambulances
    
    def find_available_ambulances(self, location: Dict[str, float], priority: int) -> List[Dict[str, Any]]:
        """
        Find available ambulances near the specified location
        
        Args:
            location: Dictionary with latitude and longitude
            priority: Patient priority level (1-5)
        
        Returns:
            List of available ambulances sorted by proximity
        """
        available = [a for a in self.ambulances if a["status"] == "Sẵn sàng"]
        
        # Calculate distances
        for ambulance in available:
            ambulance["distance"] = self._calculate_distance(
                location.get("latitude", 0),
                location.get("longitude", 0),
                ambulance["location"]["latitude"],
                ambulance["location"]["longitude"]
            )
            
            # Advanced ambulances for high priority cases
            if priority >= 4:
                ambulance["match_score"] = 100 if ambulance["equipment"].get("advanced") else 50
            else:
                ambulance["match_score"] = 80
        
        # Sort by match score (high priority) then distance
        available.sort(key=lambda x: (-x["match_score"], x["distance"]))
        return available[:5]  # Return top 5
    
    def dispatch_ambulance(self, ambulance_id: str, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Dispatch an ambulance to a patient
        
        Args:
            ambulance_id: ID of the ambulance to dispatch
            patient_data: Patient information
        
        Returns:
            Dispatch details
        """
        # Find the ambulance
        ambulance = next((a for a in self.ambulances if a["id"] == ambulance_id), None)
        if not ambulance:
            return {"success": False, "message": f"Không tìm thấy xe cấp cứu {ambulance_id}"}
        
        # Update status
        ambulance["status"] = "Đang di chuyển"
        
        # Calculate estimated arrival time
        distance_km = ambulance.get("distance", 5)  # Default to 5km if missing
        
        # Estimate 2 minutes per km + 5 minutes preparation
        travel_minutes = (distance_km * 2) + 5
        
        # Create arrival estimate
        now = datetime.now()
        arrival_time = now + timedelta(minutes=travel_minutes)
        
        return {
            "success": True,
            "ambulance_id": ambulance_id,
            "ambulance_type": ambulance["type"],
            "dispatch_time": now.strftime("%H:%M:%S"),
            "estimated_arrival": arrival_time.strftime("%H:%M:%S"),
            "travel_minutes": int(travel_minutes),
            "distance_km": round(distance_km, 1),
            "staff": ambulance["staff"],
            "message": f"Đã điều xe cấp cứu {ambulance_id}, dự kiến đến nơi sau {int(travel_minutes)} phút"
        }
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two points using a simplified formula
        For demo purposes only - a real implementation would use a proper geodesic formula
        
        Returns:
            Distance in kilometers (approximate)
        """
        # Very simple approximation for demo - would use a proper formula in production
        # Just to have some variation in the results
        x_diff = (lon2 - lon1) * 111.32 * abs(1 / (1 - 0.08 * (min(lat1, lat2) / 90)**2))
        y_diff = (lat2 - lat1) * 110.574
        
        # Add some randomness for demo purposes
        distance = (x_diff**2 + y_diff**2)**0.5
        return distance * (0.8 + random.random() * 0.4)  # Add ±20% randomness
