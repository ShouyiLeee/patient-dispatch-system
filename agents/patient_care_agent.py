"""
Patient Care Agent - Routes patients to appropriate services
Simple routing logic based on priority and symptoms
English function names with Vietnamese data only
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PatientCareAgent:
    """
    Patient Care Agent that routes patients based on severity
    Routes: QA (mild) -> Hospital (moderate) -> Emergency (severe)
    """
    
    def __init__(self):
        self.routing_thresholds = {
            "qa_max_priority": 2,       # Priority 1-2 -> QA consultation
            "hospital_max_priority": 4,  # Priority 3-4 -> Hospital
            "emergency_priority": 5      # Priority 5 -> Emergency dispatch
        }
        
        self.emergency_keywords = [
            'ngất', 'hôn mê', 'co giật', 'khó thở nặng', 'đau ngực dữ dội',
            'chảy máu nhiều', 'sốc', 'đột quỵ', 'nhồi máu'
        ]
    
    def process_patient(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process patient data and determine routing
        
        Args:
            patient_data: Patient information dictionary
            
        Returns:
            Routing decision with destination and reasoning
        """
        try:
            priority = patient_data.get('muc_do_uu_tien', patient_data.get('priority_level', 3))
            symptoms = patient_data.get('trieu_chung', patient_data.get('symptoms', []))
            description = patient_data.get('mo_ta', patient_data.get('description', ''))
            vital_signs = patient_data.get('chi_so_sinh_ton', patient_data.get('vital_signs', {}))
            
            # Check for emergency keywords in description
            is_emergency = any(keyword in description.lower() for keyword in self.emergency_keywords)
            
            # Check vital signs for emergency indicators
            if vital_signs:
                heart_rate = vital_signs.get('nhip_tim', vital_signs.get('heart_rate', 0))
                spo2 = vital_signs.get('spo2', 100)
                
                if heart_rate > 120 or heart_rate < 50 or spo2 < 90:
                    is_emergency = True
            
            # Routing decision
            if is_emergency or priority >= self.routing_thresholds["emergency_priority"]:
                route_to = "emergency"
                reason = "Trường hợp cấp cứu - cần xe cứu thương và bệnh viện ngay lập tức"
                next_step = "dispatch_then_hospital"
                
            elif priority <= self.routing_thresholds["qa_max_priority"]:
                route_to = "qa"
                reason = "Triệu chứng nhẹ - phù hợp tư vấn trực tuyến"
                next_step = "consultation"
                
            else:  # priority 3-4
                route_to = "hospital"
                reason = "Cần khám và điều trị tại bệnh viện"
                next_step = "hospital_direct"
            
            result = {
                "route_to": route_to,
                "reason": reason,
                "next_step": next_step,
                "priority_level": priority,
                "is_emergency": is_emergency,
                "recommended_specialty": patient_data.get('chuyen_khoa', patient_data.get('specialty', 'nội khoa')),
                "patient_id": patient_data.get('patient_id', 'unknown')
            }
            
            logger.info(f"Patient {result['patient_id']} routed to: {route_to} (priority: {priority})")
            return result
            
        except Exception as e:
            logger.error(f"Error in patient care routing: {e}")
            return {
                "route_to": "qa",
                "reason": "Lỗi hệ thống - chuyển sang tư vấn trực tuyến",
                "next_step": "consultation",
                "priority_level": 3,
                "is_emergency": False,
                "error": str(e)
            }
    
    # Legacy method name for compatibility
    def process(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Legacy method - calls process_patient"""
        return self.process_patient(patient_data)
