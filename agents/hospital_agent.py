import logging
import json
import os
from agents.base_agent import BaseAgent
from modules.patient_care_module.hospital_coordinator import HospitalCoordinator

class HospitalAgent(BaseAgent):
    """
    Agent responsible for hospital selection and coordination.
    """
    
    def __init__(self, message_broker, config=None):
        super().__init__(message_broker, agent_id="hospital_agent")
        
        # Initialize hospital coordinator (không truyền config)
        self.hospital_coordinator = HospitalCoordinator()
        
        # Load hospital database
        data_dir = config['system']['data_dir'] if config and 'system' in config and 'data_dir' in config['system'] else 'data'
        with open(os.path.join(data_dir, 'hospital_db.json'), 'r') as f:
            self.hospital_db = json.load(f)
    
    def _register_handlers(self):
        """Register message handlers"""
        self.message_broker.subscribe("patient_triaged", self.process_message)
        self.message_broker.subscribe("optimize_hospitals", self.process_message)
    
    def process_message(self, topic, message):
        """Process incoming messages"""
        if topic == "patient_triaged":
            patient_id = message.get("patient_id")
            priority = message.get("priority")
            specialty = message.get("specialty")
            is_emergency = message.get("is_emergency", False)
            patient_location = message.get("patient_location")
            
            self.logger.info(f"Finding hospitals for patient {patient_id} with priority {priority}")
            
            # Find suitable hospitals
            hospital_matches = self.find_hospitals(
                patient_id, 
                priority, 
                specialty, 
                is_emergency,
                patient_location
            )
            
            # Send to optimizer for ranking if emergency
            if is_emergency:
                optimize_request = {
                    "patient_id": patient_id,
                    "hospitals": hospital_matches,
                    "patient_location": patient_location,
                    "is_emergency": is_emergency,
                    "priority": priority
                }
                self.send_message("optimize_hospitals", optimize_request)
            else:
                # For non-emergency, just return the hospitals directly
                result = {
                    "patient_id": patient_id,
                    "hospitals": hospital_matches,
                    "is_emergency": is_emergency
                }
                self.send_message("hospitals_selected", result)
        
        elif topic == "optimize_hospitals":
            # This would handle optimized hospital list from the optimizer
            optimized_hospitals = message.get("optimized_hospitals")
            patient_id = message.get("patient_id")
            
            if optimized_hospitals:
                self.logger.info(f"Received optimized hospital list for patient {patient_id}")
                
                # Further process or finalize the hospital selection
                result = {
                    "patient_id": patient_id,
                    "hospitals": optimized_hospitals,
                    "is_emergency": message.get("is_emergency", False),
                    "optimized": True
                }
                self.send_message("hospitals_selected", result)
    
    def find_hospitals(self, patient_id, priority, specialty, is_emergency, location):
        """
        Find suitable hospitals based on patient needs
        
        Args:
            patient_id: Patient identifier
            priority: Patient priority level (1-5)
            specialty: Required medical specialty
            is_emergency: Whether this is an emergency case
            location: Patient's location
            
        Returns:
            List of suitable hospitals with relevant details
        """
        return self.hospital_coordinator.find_matching_hospitals(
            priority=priority,
            specialty=specialty,
            is_emergency=is_emergency,
            location=location
        )
    
    def receive_message(self, message):
        # Simple implementation to satisfy abstract method
        self.logger.info(f"HospitalAgent received message: {message}")
        # You can expand this as needed for your workflow