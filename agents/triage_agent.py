import logging
from agents.base_agent import BaseAgent
from modules.triage_module.text_processing import TextProcessor
from modules.triage_module.image_processing import ImageProcessor

class TriageAgent(BaseAgent):
    """Agent for triage (text + image) using Gemini Flash 2.0 base."""
    def __init__(self, message_broker, config=None):
        super().__init__(message_broker, agent_id="triage_agent")
        self.text_processor = TextProcessor()
        self.image_processor = ImageProcessor()

    def _register_handlers(self):
        self.message_broker.subscribe("new_patient", self.receive_message)

    def receive_message(self, topic, message):
        if topic == "new_patient":
            # Lấy đầy đủ các trường đầu vào
            desc = message.get("description", "")
            images = message.get("images", [])
            location = message.get("location", "")
            vitals = message.get("vitals", "")
            onset_time = message.get("onset_time", "")
            medical_history = message.get("medical_history", "")
            # Tổng hợp đầu vào cho text processor
            patient_info = {
                "description": desc,
                "location": location,
                "vitals": vitals,
                "onset_time": onset_time,
                "medical_history": medical_history
            }
            # Trích xuất thông tin từ mô tả + các trường khác
            state = self.text_processor.process(patient_info)
            # Trích xuất thông tin từ ảnh (nếu có)
            image_contexts = [self.image_processor.process_image(img) for img in images] if images else []
            # Tổng hợp tất cả thông tin đầu vào và trích xuất
            triage_state = {
                **state,
                "image_contexts": image_contexts,
                "location": location,
                "vitals": vitals,
                "onset_time": onset_time,
                "medical_history": medical_history,
                "raw_description": desc,
                "raw_images": images
            }
            self.send_message("patient_triaged", triage_state)
