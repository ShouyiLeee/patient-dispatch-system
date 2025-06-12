"""
Patient Care Module
Handles patient care coordination, ambulance dispatching, hospital coordination, and QA chatbot
"""

# Expose main classes for easier imports
from .qa_chatbot import QAChatbot
from .hospital_agent import HospitalAgent
from .dispatch_agent import DispatchAgent

# Optional imports if available 
try:
    from .hospital_coordinator import HospitalCoordinator
except ImportError:
    pass

try:
    from .care_manager import CareManager
except ImportError:
    pass

try:
    from .ambulance_dispatcher import AmbulanceDispatcher
except ImportError:
    pass
    
    __all__ = ['CareManager', 'AmbulanceDispatcher', 'HospitalCoordinator', 'QAChatbot']
    
except ImportError as e:
    # Fallback if some imports fail
    import logging
    logging.warning(f"Some patient care module imports failed: {e}")
    __all__ = []
