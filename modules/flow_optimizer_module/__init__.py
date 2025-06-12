"""
Flow Optimizer Module
Handles route optimization, traffic modeling, and hospital load estimation
"""

# Expose main class for easier import
try:
    from .flow_agent import FlowAgent
except ImportError:
    import logging
    logging.warning("FlowAgent import failed")
    FlowAgent = None

# Optional imports if available
try:
    from .traffic_model import TrafficModel
except ImportError:
    TrafficModel = None

try:
    from .hospital_load_estimator import HospitalLoadEstimator
except ImportError:
    HospitalLoadEstimator = None

__all__ = ['FlowAgent']
