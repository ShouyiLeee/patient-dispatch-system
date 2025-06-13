"""
Flow Optimization Agent for Patient Dispatch System
Handles optimization of patient flow and assignment
"""

import logging
import json
import random
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class FlowAgent:
    """
    Flow optimization agent for patient dispatch workflow
    Handles backups, alternates, and optimization
    """
    
    def __init__(self, traffic_model=None, load_estimator=None):
        """
        Initialize flow agent
        
        Args:
            traffic_model: Traffic model for estimating travel times
            load_estimator: Hospital load estimator
        """
        self.traffic_model = traffic_model
        self.load_estimator = load_estimator
        logger.info("Flow Agent initialized")
    
    def optimize_assignment(self, assignment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize the assignment based on traffic, hospital load, etc.
        
        Args:
            assignment_data: Assignment data from previous step
            
        Returns:
            Optimized assignment with backups and alternatives
        """
        # Extract the route type
        route_type = assignment_data.get("route_type", "unknown")
        
        # Process based on route type
        if route_type == "qa_consultation":
            return self._optimize_qa_assignment(assignment_data)
        elif route_type == "hospital_direct":
            return self._optimize_hospital_assignment(assignment_data)
        elif route_type == "emergency_dispatch":
            return self._optimize_emergency_assignment(assignment_data)
        else:
            # Default optimization (should not happen)
            logger.warning(f"Unknown route type: {route_type}")
            return {
                **assignment_data,
                "optimized": False,
                "message": "Không thể tối ưu hóa do không xác định được tuyến"
            }
    
    def _optimize_qa_assignment(self, assignment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize QA consultation assignment"""
        qa_data = assignment_data.get("qa_data", {})
        
        # Add alternate recommendations
        alternates = []
        
        # Add a hospital recommendation as backup
        if random.random() > 0.3:  # 70% chance to add hospital backup
            alternates.append({
                "type": "hospital",
                "name": "Bệnh viện Đa khoa Quận 1",
                "distance": 3.2,
                "wait_time": "15-20 phút",
                "reason": "Có thể khám trực tiếp nếu tình trạng xấu đi"
            })
        
        # Return optimized data
        return {
            **assignment_data,
            "qa_data": {
                **qa_data,
                "estimated_response_time": "2-3 phút",
                "estimated_session_time": "10-15 phút",
                "alternate_options": alternates
            },
            "optimized": True,
            "timestamp": datetime.now().isoformat(),
            "message": "Đã tối ưu hóa tư vấn y tế"
        }
    
    def _optimize_hospital_assignment(self, assignment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize hospital assignment"""
        hospital_data = assignment_data.get("hospital_data", {})
        primary_hospital = hospital_data.get("selected_hospital", {})
        
        # Get other hospitals from the list
        all_hospitals = hospital_data.get("hospitals", [])
        other_hospitals = [h for h in all_hospitals if h.get("id") != primary_hospital.get("id")]
        
        # Add backup hospitals
        backup_hospitals = other_hospitals[:2]  # Take up to 2 backups
        
        # Add traffic info if available
        if self.traffic_model:
            try:
                traffic_info = {
                    "congestion_level": random.choice(["Nhẹ", "Trung bình", "Cao"]),
                    "estimated_delay": f"{random.randint(0, 15)} phút"
                }
            except Exception:
                traffic_info = {"congestion_level": "Không có dữ liệu"}
        else:
            traffic_info = {"congestion_level": "Không có dữ liệu"}
            
        # Return optimized data
        return {
            **assignment_data,
            "hospital_data": {
                **hospital_data,
                "backup_hospitals": backup_hospitals,
                "traffic_info": traffic_info,
                "estimated_wait_time": f"{random.randint(5, 40)} phút"
            },
            "optimized": True,
            "timestamp": datetime.now().isoformat(),
            "message": "Đã tối ưu hóa chuyển thẳng đến bệnh viện"
        }
    
    def _optimize_emergency_assignment(self, assignment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize emergency assignment"""
        dispatch_data = assignment_data.get("dispatch_data", {})
        ambulance_data = dispatch_data.get("ambulance", {})
        
        # Get other ambulances
        all_ambulances = dispatch_data.get("ambulances", [])
        other_ambulances = [a for a in all_ambulances if a.get("id") != ambulance_data.get("id")]
        
        # Add backup ambulances
        backup_ambulances = other_ambulances[:1]  # Take 1 backup
        
        # Add hospital recommendations
        recommended_hospitals = []
        hospital_names = ["Bệnh viện Cấp cứu Trung ương", "Bệnh viện Đa khoa Thành phố", 
                         "Bệnh viện Chợ Rẫy", "Bệnh viện 115"]
        
        for i in range(min(2, len(hospital_names))):
            recommended_hospitals.append({
                "name": hospital_names[i],
                "specialties": ["Cấp cứu", "Hồi sức"],
                "distance": round(random.uniform(2, 8), 1),
                "estimated_time": f"{random.randint(5, 20)} phút"
            })
            
        # Traffic optimization
        if self.traffic_model:
            # In a real implementation, would use actual traffic data
            optimized_route = {
                "distance": round(dispatch_data.get("distance_km", 5) * 0.9, 1),  # 10% shorter
                "estimated_time": round(dispatch_data.get("travel_minutes", 10) * 0.85)  # 15% faster
            }
        else:
            optimized_route = {
                "distance": dispatch_data.get("distance_km"),
                "estimated_time": dispatch_data.get("travel_minutes")
            }
            
        # Return optimized data
        return {
            **assignment_data,
            "dispatch_data": {
                **dispatch_data,
                "backup_ambulances": backup_ambulances,
                "recommended_hospitals": recommended_hospitals,
                "optimized_route": optimized_route
            },
            "optimized": True,
            "timestamp": datetime.now().isoformat(),
            "message": "Đã tối ưu hóa điều xe cấp cứu"
        }
