import logging
import uuid
from typing import Dict, List, Callable, Any, Optional
from datetime import datetime
import threading
import time


class Message:
    """Message class for the broker."""
    
    def __init__(self, topic: str, content: Dict[str, Any], sender_id: Optional[str] = None):
        self.message_id = str(uuid.uuid4())
        self.topic = topic
        self.content = content
        self.sender_id = sender_id
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            "message_id": self.message_id,
            "topic": self.topic,
            "content": self.content,
            "sender_id": self.sender_id,
            "timestamp": self.timestamp.isoformat()
        }


class MessageBroker:
    """
    Facilitates communication between agents in the multi-agent system.
    Implements a publish-subscribe pattern.
    """
    
    def __init__(self):
        self.logger = logging.getLogger("MessageBroker")
        self.subscribers: Dict[str, List[Callable]] = {}
        self.agents = {}
        self.messages_history: List[Message] = []
        self.max_history = 1000  # Maximum number of messages to keep in history
        
        # Add threading support for async message delivery
        self.delivery_queue = []
        self.delivery_lock = threading.Lock()
        self.delivery_thread = threading.Thread(target=self._process_delivery_queue, daemon=True)
        self.running = True
        self.delivery_thread.start()
    
    def register_agent(self, agent):
        """Register an agent with the message broker."""
        agent_id = getattr(agent, 'agent_id', agent.__class__.__name__)
        self.agents[agent_id] = agent
        self.logger.info(f"Agent {agent_id} registered with message broker")
    
    def subscribe(self, topic: str, callback: Callable):
        """Subscribe to a topic with a callback function."""
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(callback)
        self.logger.debug(f"Added subscription for topic '{topic}'")
    
    def publish(self, topic: str, content: Dict[str, Any], sender_id: Optional[str] = None):
        """
        Publish a message to a topic.
        Messages are queued for asynchronous delivery.
        """
        message = Message(topic, content, sender_id)
        
        # Add message to history
        self.messages_history.append(message)
        if len(self.messages_history) > self.max_history:
            self.messages_history = self.messages_history[-self.max_history:]
        
        # Queue message for delivery
        with self.delivery_lock:
            self.delivery_queue.append(message)
        
        self.logger.debug(f"Message queued for topic '{topic}'")
    
    def _process_delivery_queue(self):
        """Process the delivery queue in a separate thread."""
        while self.running:
            messages_to_deliver = []
            
            # Get messages from queue
            with self.delivery_lock:
                if self.delivery_queue:
                    messages_to_deliver = self.delivery_queue.copy()
                    self.delivery_queue = []
            
            # Deliver messages
            for message in messages_to_deliver:
                self._deliver_message(message)
            
            # Sleep a short time if no messages
            if not messages_to_deliver:
                time.sleep(0.01)
    
    def _deliver_message(self, message: Message):
        """Deliver a message to all subscribers of its topic."""
        topic = message.topic
        if topic not in self.subscribers:
            self.logger.debug(f"No subscribers for topic '{topic}'")
            return
        
        for callback in self.subscribers[topic]:
            try:
                callback(topic, message.content)
            except Exception as e:
                self.logger.error(f"Error in callback for topic '{topic}': {e}")
        
        self.logger.debug(f"Delivered message to {len(self.subscribers[topic])} subscribers for topic '{topic}'")
    
    def get_history(self, topics=None, limit=None, since=None):
        """
        Get message history, optionally filtered.
        
        Args:
            topics: Optional list of topics to filter by
            limit: Optional maximum number of messages to return
            since: Optional datetime to filter messages after
            
        Returns:
            List of message dictionaries
        """
        filtered_history = self.messages_history
        
        # Filter by topics
        if topics:
            filtered_history = [msg for msg in filtered_history if msg.topic in topics]
        
        # Filter by timestamp
        if since:
            filtered_history = [msg for msg in filtered_history if msg.timestamp > since]
        
        # Apply limit
        if limit and limit > 0:
            filtered_history = filtered_history[-limit:]
        
        # Convert to dictionaries
        return [msg.to_dict() for msg in filtered_history]
    
    def shutdown(self):
        """Shut down the message broker."""
        self.running = False
        if self.delivery_thread.is_alive():
            self.delivery_thread.join(timeout=1.0)
        self.logger.info("Message broker shut down")