"""
Triage Manager - Coordinates triage activities
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)

class TriageManager:
    """
    Central coordinator for all triage activities
    Manages image processing, text analysis, and medical model integration
    """
    
    def __init__(self):
        self.image_processor = None
        self.text_processor = None
        self.medical_models = None
        
    def initialize_processors(self):
        """Initialize all processing components"""
        try:
            from .image_processing import ImageProcessor
            from .text_processing import TextProcessor
            from .medical_models import MedicalModels
            
            self.image_processor = ImageProcessor()
            self.text_processor = TextProcessor()
            self.medical_models = MedicalModels()
            
            logger.info("Triage processors initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize triage processors: {e}")
            raise
    
    def process_patient_data(self, patient_data: Dict[str, Any], image_data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Process complete patient data for triage
        
        Args:
            patient_data: Patient information and symptoms
            image_data: Optional medical images
            
        Returns:
            Complete triage analysis results
        """
        if not all([self.image_processor, self.text_processor, self.medical_models]):
            self.initialize_processors()
            
        results = {
            "patient_id": patient_data.get("patient_id"),
            "timestamp": datetime.now().isoformat(),
            "text_analysis": {},
            "image_analysis": {},
            "medical_assessment": {},
            "final_priority": 0,
            "recommended_specialty": None,
            "urgency_level": "low"
        }
        
        try:
            # Process text symptoms and description
            if patient_data.get("symptoms") or patient_data.get("description"):
                logger.info(f"Processing text data for patient {patient_data.get('patient_id')}")
                results["text_analysis"] = self.text_processor.analyze_symptoms(patient_data)
            
            # Process medical images if provided
            if image_data:
                logger.info(f"Processing image data for patient {patient_data.get('patient_id')}")
                results["image_analysis"] = self.image_processor.analyze_images(image_data)
            
            # Combine results using medical models
            logger.info(f"Generating medical assessment for patient {patient_data.get('patient_id')}")
            results["medical_assessment"] = self.medical_models.generate_assessment(
                patient_data, 
                results["text_analysis"], 
                results["image_analysis"]
            )
            
            # Determine final priority and urgency
            results["final_priority"] = self._calculate_priority(results)
            results["urgency_level"] = self._determine_urgency(results)
            results["recommended_specialty"] = self._recommend_specialty(results)
            
            logger.info(f"Triage completed for patient {patient_data.get('patient_id')} - Priority: {results['final_priority']}")
            
        except Exception as e:
            logger.error(f"Triage processing failed for patient {patient_data.get('patient_id')}: {e}")
            results["error"] = str(e)
            results["final_priority"] = 3  # Default medium priority on error
            
        return results
    
    def _calculate_priority(self, analysis_results: Dict) -> int:
        """Calculate final priority score (1-5, 5 being highest)"""
        text_priority = analysis_results.get("text_analysis", {}).get("priority", 2)
        image_priority = analysis_results.get("image_analysis", {}).get("risk_level", 2)
        medical_priority = analysis_results.get("medical_assessment", {}).get("priority", 2)
        
        # Weighted average with medical assessment having highest weight
        weights = {"text": 0.3, "image": 0.3, "medical": 0.4}
        final_priority = (
            text_priority * weights["text"] + 
            image_priority * weights["image"] + 
            medical_priority * weights["medical"]
        )
        
        return min(5, max(1, round(final_priority)))
    
    def _determine_urgency(self, analysis_results: Dict) -> str:
        """Determine urgency level based on analysis"""
        priority = self._calculate_priority(analysis_results)
        
        if priority >= 5:
            return "critical"
        elif priority >= 4:
            return "high"
        elif priority >= 3:
            return "medium"
        else:
            return "low"
    
    def _recommend_specialty(self, analysis_results: Dict) -> str:
        """Recommend medical specialty based on analysis"""
        text_specialty = analysis_results.get("text_analysis", {}).get("specialty", "general")
        image_specialty = analysis_results.get("image_analysis", {}).get("specialty", "general")
        medical_specialty = analysis_results.get("medical_assessment", {}).get("specialty", "general")
        
        # Priority: medical_assessment > image_analysis > text_analysis
        if medical_specialty and medical_specialty != "general":
            return medical_specialty
        elif image_specialty and image_specialty != "general":
            return image_specialty
        else:
            return text_specialty
