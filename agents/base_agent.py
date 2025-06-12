import logging
import uuid
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from utils.message_broker import MessageBroker


class BaseAgent(ABC):
    """Base class for all agents in the system."""
    
    def __init__(self, message_broker: MessageBroker, agent_id: str = None):
        """
        Initialize the base agent.
        
        Args:
            message_broker: Message broker for inter-agent communication
            agent_id: Optional unique identifier for the agent
        """
        self.agent_id = agent_id or f"{self.__class__.__name__}_{uuid.uuid4().hex[:8]}"
        self.message_broker = message_broker
        self.logger = logging.getLogger(f"agent.{self.agent_id}")
        self._register_handlers()
        self.logger.info(f"Agent {self.agent_id} initialized")
    
    @abstractmethod
    def _register_handlers(self):
        """Register message handlers with the message broker."""
        pass
    
    def send_message(self, topic: str, content: Dict[str, Any]):
        """
        Send message to other agents via the message broker.
        
        Args:
            topic: Message topic
            content: Message content as dictionary
        """
        self.logger.debug(f"Sending message on topic {topic}: {content}")
        self.message_broker.publish(topic, content, sender_id=self.agent_id)
    
    @abstractmethod
    def receive_message(self, topic: str, message: Dict[str, Any]):
        """
        Process received messages.
        
        Args:
            topic: Message topic
            message: Message content
        """
        pass
    
    def log_action(self, action: str, details: Optional[Dict[str, Any]] = None):
        """Log agent action for monitoring and debugging."""
        action_data = {
            "agent_id": self.agent_id,
            "action": action,
        }
        if details:
            action_data["details"] = details
        
        self.send_message("agent_action", action_data)
        self.logger.info(f"Action: {action} - {details if details else ''}")