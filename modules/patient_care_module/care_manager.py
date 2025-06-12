"""
Care Manager - Coordinates patient care activities
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class CareManager:
    """
    Central coordinator for patient care activities
    Manages the overall patient flow from triage to discharge
    """
    
    def __init__(self):
        self.ambulance_dispatcher = None
        self.hospital_coordinator = None
        self.qa_chatbot = None
        self.active_cases = {}
        
    def initialize_services(self):
        """Initialize all care services"""
        try:
            from .ambulance_dispatcher import AmbulanceDispatcher
            from .hospital_coordinator import HospitalCoordinator
            from .qa_chatbot import QAChatbot
            
            self.ambulance_dispatcher = AmbulanceDispatcher()
            self.hospital_coordinator = HospitalCoordinator()
            self.qa_chatbot = QAChatbot()
            
            logger.info("Care management services initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize care services: {e}")
            raise
    
    def create_care_plan(self, patient_data: Dict[str, Any], triage_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create comprehensive care plan based on patient data and triage results
        
        Args:
            patient_data: Patient information
            triage_results: Results from triage analysis
            
        Returns:
            Complete care plan with next steps
        """
        if not all([self.ambulance_dispatcher, self.hospital_coordinator, self.qa_chatbot]):
            self.initialize_services()
            
        care_plan_id = str(uuid.uuid4())
        priority = triage_results.get("final_priority", 2)
        urgency = triage_results.get("urgency_level", "low")
        
        care_plan = {
            "care_plan_id": care_plan_id,
            "patient_id": patient_data.get("patient_id"),
            "timestamp": datetime.now().isoformat(),
            "priority": priority,
            "urgency_level": urgency,
            "care_pathway": self._determine_care_pathway(priority, urgency),
            "transport_plan": {},
            "hospital_plan": {},
            "follow_up_plan": {},
            "status": "active"
        }
        
        try:
            logger.info(f"Creating care plan for patient {patient_data.get('patient_id')} with priority {priority}")
            
            # Determine care pathway based on priority
            if priority >= 4:  # High priority
                care_plan = self._handle_high_priority_care(care_plan, patient_data, triage_results)
            elif priority >= 3:  # Medium priority
                care_plan = self._handle_medium_priority_care(care_plan, patient_data, triage_results)
            else:  # Low priority
                care_plan = self._handle_low_priority_care(care_plan, patient_data, triage_results)
            
            # Store active case
            self.active_cases[care_plan_id] = care_plan
            
            logger.info(f"Care plan created successfully for patient {patient_data.get('patient_id')}")
            
        except Exception as e:
            logger.error(f"Failed to create care plan: {e}")
            care_plan["error"] = str(e)
            care_plan["status"] = "failed"
            
        return care_plan
    
    def _determine_care_pathway(self, priority: int, urgency: str) -> str:
        """Determine appropriate care pathway"""
        if urgency == "critical" or priority >= 5:
            return "emergency_transport"
        elif urgency == "high" or priority >= 4:
            return "urgent_transport"
        elif urgency == "medium" or priority >= 3:
            return "scheduled_transport"
        else:
            return "telehealth_consultation"
    
    def _handle_high_priority_care(self, care_plan: Dict, patient_data: Dict, triage_results: Dict) -> Dict:
        """Handle high priority patient care"""
        logger.info(f"Handling high priority care for patient {patient_data.get('patient_id')}")
        
        # Emergency transport
        transport_result = self.ambulance_dispatcher.dispatch_emergency_ambulance(
            patient_data, triage_results
        )
        care_plan["transport_plan"] = transport_result
        
        # Find emergency hospital
        hospital_result = self.hospital_coordinator.find_emergency_hospital(
            patient_data, triage_results
        )
        care_plan["hospital_plan"] = hospital_result
        
        # Coordinate immediate admission
        if hospital_result.get("hospital_id"):
            admission_result = self.hospital_coordinator.coordinate_emergency_admission(
                hospital_result["hospital_id"], patient_data, triage_results
            )
            care_plan["admission_status"] = admission_result
        
        care_plan["estimated_response_time"] = "5-10 minutes"
        care_plan["care_instructions"] = "Emergency protocol activated. Immediate transport and stabilization."
        
        return care_plan
    
    def _handle_medium_priority_care(self, care_plan: Dict, patient_data: Dict, triage_results: Dict) -> Dict:
        """Handle medium priority patient care"""
        logger.info(f"Handling medium priority care for patient {patient_data.get('patient_id')}")
        
        # Standard ambulance dispatch
        transport_result = self.ambulance_dispatcher.dispatch_standard_ambulance(
            patient_data, triage_results
        )
        care_plan["transport_plan"] = transport_result
        
        # Find appropriate hospital
        hospital_result = self.hospital_coordinator.find_suitable_hospital(
            patient_data, triage_results
        )
        care_plan["hospital_plan"] = hospital_result
        
        # Schedule admission
        if hospital_result.get("hospital_id"):
            admission_result = self.hospital_coordinator.schedule_admission(
                hospital_result["hospital_id"], patient_data, triage_results
            )
            care_plan["admission_status"] = admission_result
        
        care_plan["estimated_response_time"] = "15-30 minutes"
        care_plan["care_instructions"] = "Standard transport protocol. Monitor patient condition."
        
        return care_plan
    
    def _handle_low_priority_care(self, care_plan: Dict, patient_data: Dict, triage_results: Dict) -> Dict:
        """Handle low priority patient care"""
        logger.info(f"Handling low priority care for patient {patient_data.get('patient_id')}")
        
        # Check if telehealth consultation is appropriate
        telehealth_result = self.qa_chatbot.assess_telehealth_suitability(
            patient_data, triage_results
        )
        
        if telehealth_result.get("suitable_for_telehealth"):
            # Provide telehealth consultation
            consultation_result = self.qa_chatbot.start_consultation(
                patient_data, triage_results
            )
            care_plan["consultation_plan"] = consultation_result
            care_plan["care_pathway"] = "telehealth_consultation"
            care_plan["estimated_response_time"] = "immediate"
            care_plan["care_instructions"] = "Telehealth consultation initiated. Follow chatbot guidance."
        else:
            # Schedule non-urgent transport
            transport_result = self.ambulance_dispatcher.schedule_non_urgent_transport(
                patient_data, triage_results
            )
            care_plan["transport_plan"] = transport_result
            
            # Find clinic or urgent care
            facility_result = self.hospital_coordinator.find_urgent_care_facility(
                patient_data, triage_results
            )
            care_plan["facility_plan"] = facility_result
            
            care_plan["estimated_response_time"] = "30-60 minutes"
            care_plan["care_instructions"] = "Non-urgent transport scheduled. Continue monitoring."
        
        return care_plan
    
    def update_care_status(self, care_plan_id: str, status_update: Dict[str, Any]) -> Dict[str, Any]:
        """Update care plan status"""
        if care_plan_id not in self.active_cases:
            logger.error(f"Care plan {care_plan_id} not found")
            return {"error": "Care plan not found"}
        
        care_plan = self.active_cases[care_plan_id]
        care_plan.update(status_update)
        care_plan["last_updated"] = datetime.now().isoformat()
        
        logger.info(f"Care plan {care_plan_id} updated with status: {status_update}")
        
        return care_plan
    
    def get_care_status(self, care_plan_id: str) -> Optional[Dict[str, Any]]:
        """Get current care plan status"""
        return self.active_cases.get(care_plan_id)
    
    def complete_care_plan(self, care_plan_id: str, completion_notes: str = "") -> Dict[str, Any]:
        """Mark care plan as completed"""
        if care_plan_id not in self.active_cases:
            logger.error(f"Care plan {care_plan_id} not found")
            return {"error": "Care plan not found"}
        
        care_plan = self.active_cases[care_plan_id]
        care_plan["status"] = "completed"
        care_plan["completion_time"] = datetime.now().isoformat()
        care_plan["completion_notes"] = completion_notes
        
        logger.info(f"Care plan {care_plan_id} marked as completed")
        
        return care_plan
