import logging
from agents.base_agent import BaseAgent
from modules.patient_care_module.ambulance_dispatcher import AmbulanceDispatcher

class DispatchAgent(BaseAgent):
    """Agent for ambulance dispatch using Gemini Flash 2.0 base."""
    def __init__(self, message_broker, config=None):
        super().__init__(message_broker, agent_id="dispatch_agent")
        self.dispatcher = AmbulanceDispatcher()
        # For demo, load ambulance_db from file if available
        import os, json
        self.ambulance_db = []
        data_dir = config['system']['data_dir'] if config and 'system' in config else 'data'
        db_path = os.path.join(data_dir, 'dispatch_db.json')
        if os.path.exists(db_path):
            with open(db_path, 'r') as f:
                self.ambulance_db = json.load(f)

    def _register_handlers(self):
        self.message_broker.subscribe("patient_triaged", self.receive_message)

    def receive_message(self, topic, message):
        if topic == "patient_triaged":
            ambulances = self.dispatcher.match_ambulances(message, self.ambulance_db)
            self.send_message("dispatch_list", {"patient_id": message.get("patient_id"), "ambulances": ambulances})
