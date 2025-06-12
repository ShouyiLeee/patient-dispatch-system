"""
Triage Module
Handles medical triage, image processing, and text analysis
"""

# Expose main classes for easier imports
from .image_processing import ImageProcessor
from .text_processing import TextProcessor

# Optional imports if available
try:
    from .triage_manager import TriageManager
except ImportError:
    pass

try:
    from .medical_models import MedicalModels
except ImportError:
    pass
    
    __all__ = ['TriageManager', 'ImageProcessor', 'TextProcessor', 'MedicalModels']
    
except ImportError as e:
    # Fallback if some imports fail
    import logging
    logging.warning(f"Some triage module imports failed: {e}")
    __all__ = []
