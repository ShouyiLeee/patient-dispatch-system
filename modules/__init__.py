"""
Modules package for Patient Flow System
Complete module structure for medical triage, patient care, and flow optimization
"""

# Import all main modules with error handling
try:
    from .triage_module import TriageManager, ImageProcessor, TextProcessor, MedicalModels
    TRIAGE_AVAILABLE = True
except ImportError as e:
    import logging
    logging.warning(f"Triage module import failed: {e}")
    TRIAGE_AVAILABLE = False

try:
    from .patient_care_module import CareManager, AmbulanceDispatcher, HospitalCoordinator, QAChatbot
    PATIENT_CARE_AVAILABLE = True
except ImportError as e:
    import logging
    logging.warning(f"Patient care module import failed: {e}")
    PATIENT_CARE_AVAILABLE = False

try:
    from .flow_optimizer_module import FlowAgent, TrafficModel, HospitalLoadEstimator
    FLOW_OPTIMIZER_AVAILABLE = True
except ImportError as e:
    import logging
    logging.warning(f"Flow optimizer module import failed: {e}")
    FLOW_OPTIMIZER_AVAILABLE = False

__version__ = "1.0.0"

# Dynamic __all__ based on what's available
__all__ = []

if TRIAGE_AVAILABLE:
    __all__.extend(['TriageManager', 'ImageProcessor', 'TextProcessor', 'MedicalModels'])

if PATIENT_CARE_AVAILABLE:
    __all__.extend(['CareManager', 'AmbulanceDispatcher', 'HospitalCoordinator', 'QAChatbot'])

if FLOW_OPTIMIZER_AVAILABLE:
    __all__.extend(['FlowAgent', 'TrafficModel', 'HospitalLoadEstimator'])