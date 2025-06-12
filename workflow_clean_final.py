"""
Clean Patient Dispatch Workflow
Architecture: Input -> Triage Agent -> Patient Care Agent -> (QA/Hospital/Dispatch->Hospital)
English function names with Vietnamese data only
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

# Setup logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import modules
from modules.gemini_client import GeminiClient
from modules.triage_module.text_processing import TextProcessor
from modules.triage_module.image_processing import ImageProcessor
from modules.patient_care_module.qa_chatbot import QAChatbot
from modules.patient_care_module.hospital_agent import HospitalAgent
from modules.patient_care_module.dispatch_agent import DispatchAgent
from modules.flow_optimizer_module.flow_agent import FlowAgent

class PatientDispatchWorkflow:
    """Main workflow class for patient dispatch system"""
    
    def __init__(self):
        # Initialize Gemini client
        self.gemini = GeminiClient()
        
        # Initialize all agents with English names
        self.text_processor = TextProcessor(self.gemini)
        self.image_processor = ImageProcessor(self.gemini)
        self.qa_chatbot = QAChatbot(self.gemini)
        self.hospital_agent = HospitalAgent(self.gemini)
        self.dispatch_agent = DispatchAgent(self.gemini)
        self.flow_optimizer = FlowAgent()
        
        # Progress tracking
        self.current_step = 0
        self.total_steps = 5
        
    def process_patient_input(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main workflow function - processes patient from input to final routing
        
        Args:
            patient_data: Dictionary containing patient information
            
        Returns:
            Complete workflow result with all steps
        """
        workflow_result = {
            "workflow_id": f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "start_time": datetime.now().isoformat(),
            "steps": {},
            "final_result": None,
            "status": "processing"
        }
        
        try:
            # Step 1: Extract symptoms from text and image
            logger.info("Step 1: Extracting patient information")
            step1_result = self.extract_patient_information(patient_data)
            workflow_result["steps"]["step1_extraction"] = step1_result
            
            # Step 2: Triage assessment
            logger.info("Step 2: Performing triage assessment")
            step2_result = self.perform_triage_assessment(step1_result)
            workflow_result["steps"]["step2_triage"] = step2_result
            
            # Step 3: Patient care routing decision
            logger.info("Step 3: Making routing decision")
            step3_result = self.make_routing_decision(step2_result)
            workflow_result["steps"]["step3_routing"] = step3_result
            
            # Step 4: Execute routing (QA/Hospital/Emergency)
            logger.info("Step 4: Executing routing")
            step4_result = self.execute_routing(step3_result, patient_data)
            workflow_result["steps"]["step4_execution"] = step4_result
            
            # Step 5: Final optimization and assignment
            logger.info("Step 5: Final optimization")
            step5_result = self.optimize_assignment(step4_result)
            workflow_result["steps"]["step5_optimization"] = step5_result
            
            workflow_result["final_result"] = step5_result
            workflow_result["status"] = "completed"
            workflow_result["end_time"] = datetime.now().isoformat()
            
            return workflow_result
            
        except Exception as e:
            logger.error(f"Workflow error: {e}")
            workflow_result["status"] = "error"
            workflow_result["error"] = str(e)
            workflow_result["end_time"] = datetime.now().isoformat()
            return workflow_result
    
    def extract_patient_information(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Step 1: Extract and process patient information"""
        try:
            # Process text description
            text_result = {}
            if patient_data.get("description"):
                text_result = self.text_processor.extract_symptoms(patient_data["description"])
            
            # Process image if available
            image_result = {}
            if patient_data.get("image_data"):
                image_result = self.image_processor.analyze_image(patient_data["image_data"])
            
            # Combine vital signs
            vital_signs = patient_data.get("vital_signs", {})
            
            return {
                "success": True,
                "text_analysis": text_result,
                "image_analysis": image_result,
                "vital_signs": vital_signs,
                "location": patient_data.get("location", {}),
                "extracted_symptoms": text_result.get("symptoms", []),
                "severity_indicators": self.check_severity_indicators(text_result, vital_signs)
            }
            
        except Exception as e:
            logger.error(f"Information extraction error: {e}")
            return {
                "success": False,
                "error": str(e),
                "extracted_symptoms": [],
                "severity_indicators": []
            }
    
    def perform_triage_assessment(self, extraction_result: Dict[str, Any]) -> Dict[str, Any]:
        """Step 2: Assess patient priority and urgency"""
        try:
            symptoms = extraction_result.get("extracted_symptoms", [])
            vital_signs = extraction_result.get("vital_signs", {})
            severity_indicators = extraction_result.get("severity_indicators", [])
            
            # Calculate priority score (1-5, where 5 is most urgent)
            priority_score = self.calculate_priority_score(symptoms, vital_signs, severity_indicators)
            
            # Determine urgency level
            if priority_score >= 5:
                urgency_level = "Cấp cứu"
                recommended_action = "Cần xe cấp cứu ngay lập tức"
            elif priority_score >= 3:
                urgency_level = "Khẩn cấp"
                recommended_action = "Cần đưa đến bệnh viện"
            else:
                urgency_level = "Không khẩn cấp"
                recommended_action = "Có thể tư vấn trực tuyến trước"
            
            return {
                "success": True,
                "priority_score": priority_score,
                "urgency_level": urgency_level,
                "recommended_action": recommended_action,
                "triage_notes": f"Đánh giá dựa trên {len(symptoms)} triệu chứng và chỉ số sinh tồn"
            }
            
        except Exception as e:
            logger.error(f"Triage assessment error: {e}")
            return {
                "success": False,
                "priority_score": 2,  # Default safe priority
                "urgency_level": "Không khẩn cấp",
                "recommended_action": "Tư vấn trực tuyến",
                "error": str(e)
            }
    
    def make_routing_decision(self, triage_result: Dict[str, Any]) -> Dict[str, Any]:
        """Step 3: Decide routing based on triage assessment"""
        try:
            priority_score = triage_result.get("priority_score", 2)
            urgency_level = triage_result.get("urgency_level", "Không khẩn cấp")
            
            # Routing logic
            if priority_score >= 5:
                route_type = "emergency_dispatch"
                route_description = "Chuyển đến điều phối cấp cứu"
                next_agent = "dispatch_agent"
            elif priority_score >= 3:
                route_type = "hospital_direct"
                route_description = "Chuyển trực tiếp đến bệnh viện"
                next_agent = "hospital_agent"
            else:
                route_type = "qa_consultation"
                route_description = "Tư vấn trực tuyến với chuyên gia"
                next_agent = "qa_chatbot"
            
            return {
                "success": True,
                "route_type": route_type,
                "route_description": route_description,
                "next_agent": next_agent,
                "priority_score": priority_score,
                "urgency_level": urgency_level,
                "routing_reason": f"Dựa trên mức độ ưu tiên {priority_score}/5"
            }
            
        except Exception as e:
            logger.error(f"Routing decision error: {e}")
            return {
                "success": False,
                "route_type": "qa_consultation",
                "route_description": "Tư vấn trực tuyến (mặc định)",
                "next_agent": "qa_chatbot",
                "error": str(e)
            }
    
    def execute_routing(self, routing_result: Dict[str, Any], patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Step 4: Execute the routing decision"""
        try:
            route_type = routing_result.get("route_type")
            next_agent = routing_result.get("next_agent")
            
            if next_agent == "dispatch_agent":
                # Emergency dispatch
                result = self.handle_emergency_dispatch(patient_data, routing_result)
            elif next_agent == "hospital_agent":
                # Hospital routing
                result = self.handle_hospital_routing(patient_data, routing_result)
            else:
                # QA consultation
                result = self.handle_qa_consultation(patient_data, routing_result)
            
            result["route_type"] = route_type
            result["agent_used"] = next_agent
            return result
            
        except Exception as e:
            logger.error(f"Routing execution error: {e}")
            return {
                "success": False,
                "route_type": "qa_consultation",
                "agent_used": "qa_chatbot",
                "result": "Có lỗi xảy ra, chuyển sang tư vấn trực tuyến",
                "error": str(e)
            }
    
    def handle_emergency_dispatch(self, patient_data: Dict[str, Any], routing_result: Dict[str, Any]) -> Dict[str, Any]:
        """Handle emergency dispatch routing"""
        try:
            # Get available ambulances
            ambulances = self.dispatch_agent.find_ambulance(
                location=patient_data.get("location", {}),
                priority=routing_result.get("priority_score", 5),
                is_emergency=True
            )
            
            if ambulances:
                best_ambulance = ambulances[0]
                return {
                    "success": True,
                    "type": "emergency_dispatch",
                    "ambulance_assigned": best_ambulance,
                    "estimated_arrival": f"{best_ambulance.get('eta_minutes', 5)} phút",
                    "paramedic": best_ambulance.get("paramedic", "Chưa xác định"),
                    "message": f"Xe cấp cứu {best_ambulance.get('vehicle_id')} đang trên đường đến"
                }
            else:
                return {
                    "success": False,
                    "type": "emergency_dispatch",
                    "message": "Không có xe cấp cứu khả dụng, đang liên hệ bệnh viện gần nhất"
                }
                
        except Exception as e:
            logger.error(f"Emergency dispatch error: {e}")
            return {
                "success": False,
                "type": "emergency_dispatch",
                "message": "Lỗi hệ thống điều phối, vui lòng gọi 115",
                "error": str(e)
            }
    
    def handle_hospital_routing(self, patient_data: Dict[str, Any], routing_result: Dict[str, Any]) -> Dict[str, Any]:
        """Handle direct hospital routing"""
        try:
            # Find suitable hospitals
            hospitals = self.hospital_agent.find_hospital(
                location=patient_data.get("location", {}),
                specialty=self.determine_required_specialty(patient_data),
                priority=routing_result.get("priority_score", 3)
            )
            
            if hospitals:
                best_hospital = hospitals[0]
                return {
                    "success": True,
                    "type": "hospital_direct",
                    "hospital_assigned": best_hospital,
                    "estimated_time": f"{best_hospital.get('distance', 0) * 3} phút di chuyển",
                    "available_doctor": best_hospital.get("available_doctor", "Bác sĩ trực"),
                    "message": f"Bệnh viện {best_hospital.get('name')} có thể tiếp nhận"
                }
            else:
                return {
                    "success": False,
                    "type": "hospital_direct",
                    "message": "Không tìm thấy bệnh viện phù hợp, chuyển sang tư vấn trực tuyến"
                }
                
        except Exception as e:
            logger.error(f"Hospital routing error: {e}")
            return {
                "success": False,
                "type": "hospital_direct",
                "message": "Lỗi tìm kiếm bệnh viện, chuyển sang tư ván trực tuyến",
                "error": str(e)
            }
    
    def handle_qa_consultation(self, patient_data: Dict[str, Any], routing_result: Dict[str, Any]) -> Dict[str, Any]:
        """Handle QA consultation routing"""
        try:
            # Create initial consultation context
            context = f"""Bệnh nhân có triệu chứng: {patient_data.get('description', 'Chưa mô tả')}
Mức độ ưu tiên: {routing_result.get('priority_score', 1)}/5
Khuyến nghị: Tư vấn trực tuyến"""
            
            # Initial response
            initial_response = self.qa_chatbot.ask_question(
                "Xin chào, tôi có thể giúp gì cho bạn về tình trạng sức khỏe hiện tại?",
                context
            )
            
            return {
                "success": True,
                "type": "qa_consultation",
                "consultation_started": True,
                "initial_response": initial_response.get("answer", "Xin chào, tôi sẵn sàng tư vấn cho bạn."),
                "chat_context": context,
                "message": "Đã kết nối với chuyên gia tư vấn y tế"
            }
            
        except Exception as e:
            logger.error(f"QA consultation error: {e}")
            return {
                "success": False,
                "type": "qa_consultation",
                "message": "Lỗi kết nối tư vấn, vui lòng thử lại",
                "error": str(e)
            }
    
    def optimize_assignment(self, execution_result: Dict[str, Any]) -> Dict[str, Any]:
        """Step 5: Final optimization and confirmation"""
        try:
            route_type = execution_result.get("type")
            
            if route_type == "emergency_dispatch":
                # For emergency, also find backup hospital
                backup_hospitals = self.hospital_agent.find_hospital(
                    location={}, specialty="cấp cứu", priority=5
                )
                execution_result["backup_hospital"] = backup_hospitals[0] if backup_hospitals else None
                
            elif route_type == "hospital_direct":
                # For hospital routing, optimize the selection
                hospital = execution_result.get("hospital_assigned")
                if hospital:
                    optimized = self.flow_optimizer.optimize([hospital])
                    execution_result["optimization_notes"] = optimized.get("reason", "Đã tối ưu hóa")
            
            execution_result["final_status"] = "Hoàn thành điều phối"
            execution_result["completion_time"] = datetime.now().isoformat()
            
            return execution_result
            
        except Exception as e:
            logger.error(f"Optimization error: {e}")
            execution_result["optimization_error"] = str(e)
            return execution_result
    
    # Helper methods
    def check_severity_indicators(self, text_result: Dict, vital_signs: Dict) -> List[str]:
        """Check for severity indicators in symptoms and vital signs"""
        indicators = []
        
        # Check vital signs
        if vital_signs.get("heart_rate", 0) > 100:
            indicators.append("Nhịp tim nhanh")
        if vital_signs.get("spo2", 100) < 95:
            indicators.append("SpO2 thấp")
        
        # Check symptoms for emergency keywords
        description = text_result.get("original_text", "").lower()
        emergency_keywords = ["khó thở", "đau ngực", "choáng váng", "bất tỉnh", "co giật"]
        
        for keyword in emergency_keywords:
            if keyword in description:
                indicators.append(f"Triệu chứng khẩn cấp: {keyword}")
        
        return indicators
    
    def calculate_priority_score(self, symptoms: List, vital_signs: Dict, severity_indicators: List) -> int:
        """Calculate priority score from 1-5"""
        score = 1
        
        # Base score from number of symptoms
        score += min(len(symptoms) // 2, 1)
        
        # Add score for severity indicators
        score += min(len(severity_indicators), 2)
        
        # Vital signs impact
        if vital_signs.get("heart_rate", 0) > 120:
            score += 1
        if vital_signs.get("spo2", 100) < 90:
            score += 2
        
        return min(score, 5)
    
    def determine_required_specialty(self, patient_data: Dict) -> str:
        """Determine required medical specialty"""
        description = patient_data.get("description", "").lower()
        
        if any(word in description for word in ["tim", "ngực", "huyết áp"]):
            return "tim mạch"
        elif any(word in description for word in ["phổi", "ho", "khó thở"]):
            return "hô hấp"
        elif any(word in description for word in ["dạ dày", "bụng", "tiêu hóa"]):
            return "tiêu hóa"
        else:
            return "nội tổng hợp"


def run_workflow_demo():
    """Demo function to test the complete workflow"""
    logger.info("=== DEMO PATIENT DISPATCH WORKFLOW ===")
    
    # Initialize workflow
    workflow = PatientDispatchWorkflow()
    
    # Test case 1: Normal case
    print("\n1. TEST CASE: Bệnh nhân thông thường")
    normal_patient = {
        "description": "Bệnh nhân nam, 35 tuổi, sốt nhẹ 2 ngày, ho khan, không khó thở",
        "location": {"latitude": 10.77, "longitude": 106.67},
        "vital_signs": {"heart_rate": 88, "blood_pressure": "120/80", "spo2": 98}
    }
    
    result1 = workflow.process_patient_input(normal_patient)
    print(f"Kết quả: {result1['final_result']['type']} - {result1['final_result'].get('message', 'N/A')}")
    
    # Test case 2: Emergency case
    print("\n2. TEST CASE: Bệnh nhân cấp cứu")
    emergency_patient = {
        "description": "Bệnh nhân nữ, 60 tuổi, đau ngực dữ dội, khó thở, choáng váng",
        "location": {"latitude": 10.78, "longitude": 106.68},
        "vital_signs": {"heart_rate": 130, "blood_pressure": "180/110", "spo2": 88}
    }
    
    result2 = workflow.process_patient_input(emergency_patient)
    print(f"Kết quả: {result2['final_result']['type']} - {result2['final_result'].get('message', 'N/A')}")
    
    # Test case 3: Hospital case
    print("\n3. TEST CASE: Bệnh nhân cần đến bệnh viện")
    hospital_patient = {
        "description": "Bệnh nhân nam, 45 tuổi, đau bụng dữ dội từ sáng, nôn mửa nhiều",
        "location": {"latitude": 10.76, "longitude": 106.66},
        "vital_signs": {"heart_rate": 105, "blood_pressure": "140/90", "spo2": 95}
    }
    
    result3 = workflow.process_patient_input(hospital_patient)
    print(f"Kết quả: {result3['final_result']['type']} - {result3['final_result'].get('message', 'N/A')}")
    
    print("\n=== DEMO HOÀN THÀNH ===")
    return [result1, result2, result3]


if __name__ == "__main__":
    run_workflow_demo()
