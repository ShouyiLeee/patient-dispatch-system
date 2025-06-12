"""
Hospital Load Estimator - Predicts hospital load and capacity
"""

import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)

class HospitalLoadEstimator:
    """Estimates and predicts hospital load for optimization decisions"""
    
    def __init__(self):
        self.hospital_loads = self._initialize_hospital_loads()
        
    def _initialize_hospital_loads(self) -> Dict[str, Dict[str, Any]]:
        """Initialize hospital load simulation data"""
        return {
            "HOSP001": {
                "occupancy_rate": 0.75,
                "emergency_wait_time": 15,
                "trend": "stable",
                "predicted_load": 0.78
            },
            "HOSP002": {
                "occupancy_rate": 0.60,
                "emergency_wait_time": 8,
                "trend": "decreasing", 
                "predicted_load": 0.55
            },
            "HOSP003": {
                "occupancy_rate": 0.85,
                "emergency_wait_time": 25,
                "trend": "increasing",
                "predicted_load": 0.90
            },
            "HOSP004": {
                "occupancy_rate": 0.70,
                "emergency_wait_time": 12,
                "trend": "stable",
                "predicted_load": 0.72
            },
            "HOSP005": {
                "occupancy_rate": 0.45,
                "emergency_wait_time": 5,
                "trend": "stable",
                "predicted_load": 0.47
            }
        }
    
    def estimate_hospital_load(self, hospital_id: str) -> Dict[str, Any]:
        """Estimate current hospital load"""
        if hospital_id not in self.hospital_loads:
            return {
                "occupancy_rate": 0.7,
                "emergency_wait_time": 15,
                "trend": "unknown",
                "predicted_load": 0.7,
                "confidence": 0.5
            }
        
        load_data = self.hospital_loads[hospital_id].copy()
        load_data["confidence"] = 0.85
        load_data["last_updated"] = datetime.now().isoformat()
        
        return load_data
    
    def predict_future_load(self, hospital_id: str, hours_ahead: int = 2) -> Dict[str, Any]:
        """Predict hospital load in the future"""
        current_load = self.estimate_hospital_load(hospital_id)
        
        # Simple prediction based on trend
        current_occupancy = current_load["occupancy_rate"]
        trend = current_load["trend"]
        
        if trend == "increasing":
            predicted_occupancy = min(0.95, current_occupancy + (hours_ahead * 0.05))
        elif trend == "decreasing":
            predicted_occupancy = max(0.3, current_occupancy - (hours_ahead * 0.05))
        else:  # stable
            predicted_occupancy = current_occupancy + random.uniform(-0.05, 0.05)
        
        return {
            "hospital_id": hospital_id,
            "predicted_time": (datetime.now() + timedelta(hours=hours_ahead)).isoformat(),
            "predicted_occupancy_rate": round(predicted_occupancy, 2),
            "confidence": 0.7
        }
    
    def get_all_hospital_loads(self) -> List[Dict[str, Any]]:
        """Get load estimates for all hospitals"""
        loads = []
        for hospital_id in self.hospital_loads:
            load_data = self.estimate_hospital_load(hospital_id)
            load_data["hospital_id"] = hospital_id
            loads.append(load_data)
        return loads
    
    def update_hospital_load(self, hospital_id: str, new_load_data: Dict[str, Any]):
        """Update hospital load data"""
        if hospital_id in self.hospital_loads:
            self.hospital_loads[hospital_id].update(new_load_data)
            logger.info(f"Updated load data for hospital {hospital_id}")
        else:
            self.hospital_loads[hospital_id] = new_load_data
            logger.info(f"Added new hospital load data for {hospital_id}")
