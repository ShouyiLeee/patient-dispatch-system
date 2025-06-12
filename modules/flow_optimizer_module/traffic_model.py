"""
Traffic Model - Model for simulating and using traffic data
"""

import logging
from typing import Dict, Any, List, Tuple
from datetime import datetime
import math
import random

logger = logging.getLogger(__name__)

class TrafficModel:
    """Simulates and models traffic conditions for route optimization"""
    
    def __init__(self):
        self.traffic_data = self._initialize_traffic_data()
        
    def _initialize_traffic_data(self) -> Dict[str, Any]:
        """Initialize traffic simulation data"""
        return {
            "current_conditions": "moderate",
            "congestion_areas": [
                {"lat": 10.7773, "lng": 106.6655, "level": "high"},
                {"lat": 10.7823, "lng": 106.6575, "level": "moderate"}
            ],
            "rush_hour": self._is_rush_hour()
        }
    
    def estimate_travel_time(self, start: Tuple[float, float], end: Tuple[float, float], priority: int) -> int:
        """Estimate travel time between two points"""
        distance = self._calculate_distance(start, end)
        
        # Base speed (km/h) based on priority and traffic
        if priority >= 4:  # Emergency
            base_speed = 50
        else:
            base_speed = 35
            
        # Adjust for traffic
        traffic_factor = 1.2 if self.traffic_data["rush_hour"] else 1.0
        
        time_hours = (distance / base_speed) * traffic_factor
        return max(5, int(time_hours * 60))  # Minimum 5 minutes
    
    def get_route_details(self, start: Tuple[float, float], end: Tuple[float, float], priority: int) -> Dict[str, Any]:
        """Get detailed route information"""
        distance = self._calculate_distance(start, end)
        time = self.estimate_travel_time(start, end, priority)
        
        return {
            "distance_km": round(distance, 2),
            "time_minutes": time,
            "traffic_level": "moderate",
            "route_quality": "good"
        }
    
    def get_alternative_route(self, ambulance_loc: Tuple, patient_loc: Tuple, hospital_loc: Tuple, route_type: str) -> Dict[str, Any]:
        """Get alternative route options"""
        total_distance = self._calculate_distance(ambulance_loc, patient_loc) + self._calculate_distance(patient_loc, hospital_loc)
        
        if route_type == "avoid_traffic":
            time_minutes = int(total_distance * 2.5)  # Slower but avoids traffic
        else:  # shortest_distance
            time_minutes = int(total_distance * 2.0)  # Faster but may have traffic
            
        return {"time_minutes": time_minutes, "distance_km": total_distance}
    
    def get_current_traffic_conditions(self) -> List[Dict[str, Any]]:
        """Get current traffic conditions"""
        return [
            {"area": "City Center", "level": "moderate", "delay_minutes": 5},
            {"area": "Highway", "level": "light", "delay_minutes": 2}
        ]
    
    def _calculate_distance(self, loc1: Tuple[float, float], loc2: Tuple[float, float]) -> float:
        """Calculate distance between locations (km)"""
        lat1, lng1 = loc1
        lat2, lng2 = loc2
        lat_diff = abs(lat2 - lat1) * 111
        lng_diff = abs(lng2 - lng1) * 111 * math.cos(math.radians((lat1 + lat2) / 2))
        return math.sqrt(lat_diff**2 + lng_diff**2)
    
    def _is_rush_hour(self) -> bool:
        """Check if current time is rush hour"""
        current_hour = datetime.now().hour
        return current_hour in [7, 8, 9, 17, 18, 19]
