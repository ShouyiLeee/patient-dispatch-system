import logging
from agents.base_agent import BaseAgent
from modules.flow_optimizer_module.flow_manager import FlowManager

class OptimizerAgent(BaseAgent):
    """Agent for flow optimization (pass-through for now)."""
    def __init__(self, message_broker, config=None):
        super().__init__(message_broker, agent_id="optimizer_agent")
        self.flow_manager = FlowManager()

    def _register_handlers(self):
        self.message_broker.subscribe("hospitals_selected", self.receive_message)
        self.message_broker.subscribe("dispatch_list", self.receive_message)

    def receive_message(self, topic, message):
        # For demo, just pass through the list
        if topic in ("hospitals_selected", "dispatch_list"):
            optimized = self.flow_manager.optimize(message.get('hospitals') or message.get('ambulances') or [])
            self.send_message(f"optimized_{topic}", {**message, "optimized": optimized})
