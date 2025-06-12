"""
Medical Models Module
Wrappers for multimodal and medical LLMs
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class MedicalModels:
    """
    Wrapper for multimodal and medical AI models
    Provides unified interface for different medical AI services
    """
    
    def __init__(self):
        self.multimodal_model = MultimodalMedicalModel()
        self.text_model = MedicalTextModel()
        self.image_model = MedicalImageModel()
        
    def generate_assessment(self, patient_data: Dict[str, Any], 
                          text_analysis: Dict[str, Any], 
                          image_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive medical assessment using AI models
        
        Args:
            patient_data: Original patient information
            text_analysis: Results from text processing
            image_analysis: Results from image processing
            
        Returns:
            Complete AI-generated medical assessment
        """
        assessment = {
            "timestamp": datetime.now().isoformat(),
            "model_version": "medical_ai_v1.0",
            "priority": 2,
            "confidence": 0.0,
            "specialty": "general",
            "clinical_reasoning": "",
            "differential_diagnosis": [],
            "recommended_actions": [],
            "risk_factors": [],
            "follow_up": ""
        }
        
        try:
            logger.info(f"Generating medical assessment for patient {patient_data.get('patient_id')}")
            
            # Use multimodal model if both text and image data available
            if text_analysis.get("extracted_symptoms") and image_analysis.get("findings"):
                logger.info("Using multimodal analysis")
                assessment = self.multimodal_model.analyze_multimodal(
                    patient_data, text_analysis, image_analysis
                )
            
            # Use text-only model if only text data available
            elif text_analysis.get("extracted_symptoms"):
                logger.info("Using text-only analysis")
                assessment = self.text_model.analyze_text_symptoms(
                    patient_data, text_analysis
                )
            
            # Use image-only model if only image data available
            elif image_analysis.get("findings"):
                logger.info("Using image-only analysis")
                assessment = self.image_model.analyze_medical_images(
                    patient_data, image_analysis
                )
            
            # Fallback to basic assessment
            else:
                logger.info("Using fallback basic assessment")
                assessment = self._generate_basic_assessment(patient_data)
            
            # Validate and enhance assessment
            assessment = self._validate_assessment(assessment)
            
            logger.info(f"Medical assessment completed - Priority: {assessment['priority']}")
            
        except Exception as e:
            logger.error(f"Medical assessment generation failed: {e}")
            assessment["error"] = str(e)
            assessment["priority"] = 3  # Default medium priority on error
            assessment["confidence"] = 0.3
            
        return assessment
    
    def _generate_basic_assessment(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate basic assessment when AI models are not available"""
        return {
            "timestamp": datetime.now().isoformat(),
            "model_version": "basic_assessment_v1.0",
            "priority": 2,
            "confidence": 0.5,
            "specialty": "general",
            "clinical_reasoning": "Basic triage assessment based on available information",
            "differential_diagnosis": ["General medical evaluation needed"],
            "recommended_actions": ["Clinical examination", "Vital signs assessment"],
            "risk_factors": [],
            "follow_up": "Schedule appropriate medical consultation"
        }
    
    def _validate_assessment(self, assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and ensure assessment completeness"""
        # Ensure priority is within valid range
        assessment["priority"] = max(1, min(5, assessment.get("priority", 2)))
        
        # Ensure confidence is within valid range
        assessment["confidence"] = max(0.0, min(1.0, assessment.get("confidence", 0.5)))
        
        # Ensure required fields exist
        if not assessment.get("clinical_reasoning"):
            assessment["clinical_reasoning"] = "Assessment based on available clinical data"
        
        if not assessment.get("recommended_actions"):
            assessment["recommended_actions"] = ["Further clinical evaluation recommended"]
            
        return assessment


class MultimodalMedicalModel:
    """Handles analysis using both text and image data"""
    
    def analyze_multimodal(self, patient_data: Dict[str, Any], 
                          text_analysis: Dict[str, Any], 
                          image_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze using both text and image modalities"""
        
        # Simulate advanced multimodal AI analysis
        # In real implementation, this would call actual medical AI models
        
        text_priority = text_analysis.get("priority", 2)
        image_risk = image_analysis.get("overall_risk_level", 2)
        
        # Combine priorities with weighted approach
        combined_priority = round((text_priority * 0.6 + image_risk * 0.4))
        
        # Extract key findings
        symptoms = text_analysis.get("extracted_symptoms", [])
        image_findings = image_analysis.get("findings", [])
        
        # Generate clinical reasoning
        reasoning_parts = []
        
        if symptoms:
            symptom_categories = [s.get("category") for s in symptoms]
            reasoning_parts.append(f"Patient presents with {', '.join(set(symptom_categories))}")
        
        if image_findings:
            reasoning_parts.append(f"Imaging reveals {len(image_findings)} significant findings")
        
        clinical_reasoning = ". ".join(reasoning_parts) if reasoning_parts else "Multimodal assessment performed"
        
        # Determine specialty
        text_specialty = text_analysis.get("specialty", "general")
        image_specialty = image_analysis.get("specialty", "general")
        
        # Prioritize image-based specialty if available
        final_specialty = image_specialty if image_specialty != "general" else text_specialty
        
        return {
            "timestamp": datetime.now().isoformat(),
            "model_version": "multimodal_medical_v1.0",
            "priority": combined_priority,
            "confidence": 0.85,
            "specialty": final_specialty,
            "clinical_reasoning": clinical_reasoning,
            "differential_diagnosis": self._generate_differential_diagnosis(symptoms, image_findings),
            "recommended_actions": self._generate_recommendations(combined_priority, final_specialty),
            "risk_factors": self._identify_risk_factors(patient_data, symptoms),
            "follow_up": self._determine_follow_up(combined_priority, final_specialty)
        }
    
    def _generate_differential_diagnosis(self, symptoms: List[Dict], image_findings: List[Dict]) -> List[str]:
        """Generate differential diagnosis based on symptoms and imaging"""
        diagnoses = []
        
        # Basic symptom-based diagnoses
        symptom_categories = [s.get("category") for s in symptoms]
        
        if "pain" in symptom_categories and "fever" in symptom_categories:
            diagnoses.append("Infectious process")
        
        if "breathing" in symptom_categories:
            diagnoses.append("Respiratory condition")
        
        if "headache" in symptom_categories:
            diagnoses.append("Neurological condition")
        
        # Image-based diagnoses
        for finding in image_findings:
            if "fracture" in finding.get("type", "").lower():
                diagnoses.append("Bone fracture")
            elif "lesion" in finding.get("type", "").lower():
                diagnoses.append("Space-occupying lesion")
        
        return diagnoses if diagnoses else ["General medical condition"]
    
    def _generate_recommendations(self, priority: int, specialty: str) -> List[str]:
        """Generate recommendations based on priority and specialty"""
        recommendations = []
        
        if priority >= 4:
            recommendations.append("Urgent medical evaluation")
            recommendations.append("Continuous monitoring")
        elif priority >= 3:
            recommendations.append("Timely medical assessment")
            recommendations.append("Regular follow-up")
        else:
            recommendations.append("Routine medical evaluation")
        
        # Specialty-specific recommendations
        specialty_recs = {
            "cardiology": ["ECG", "Cardiac markers", "Echocardiogram"],
            "neurology": ["Neurological examination", "Brain imaging", "Cognitive assessment"],
            "orthopedics": ["X-ray imaging", "Physical therapy evaluation"],
            "emergency": ["Immediate intervention", "Stabilization protocols"]
        }
        
        if specialty in specialty_recs:
            recommendations.extend(specialty_recs[specialty])
        
        return recommendations
    
    def _identify_risk_factors(self, patient_data: Dict, symptoms: List[Dict]) -> List[str]:
        """Identify risk factors from patient data and symptoms"""
        risk_factors = []
        
        # Age-based risk factors
        age = patient_data.get("age", 0)
        if age > 65:
            risk_factors.append("Advanced age")
        elif age < 2:
            risk_factors.append("Pediatric patient")
        
        # Symptom-based risk factors
        severe_symptoms = [s for s in symptoms if s.get("severity") == "severe"]
        if severe_symptoms:
            risk_factors.append("Severe symptom presentation")
        
        # Medical history
        if patient_data.get("medical_history"):
            risk_factors.append("Pre-existing medical conditions")
        
        return risk_factors
    
    def _determine_follow_up(self, priority: int, specialty: str) -> str:
        """Determine appropriate follow-up based on priority and specialty"""
        if priority >= 4:
            return "Immediate specialist consultation required"
        elif priority >= 3:
            return f"Follow-up with {specialty} within 24-48 hours"
        else:
            return f"Routine {specialty} consultation as appropriate"


class MedicalTextModel:
    """Handles text-only medical analysis"""
    
    def analyze_text_symptoms(self, patient_data: Dict[str, Any], 
                             text_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze symptoms using text-only AI model"""
        
        symptoms = text_analysis.get("extracted_symptoms", [])
        priority = text_analysis.get("priority", 2)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "model_version": "text_medical_v1.0",
            "priority": priority,
            "confidence": 0.75,
            "specialty": text_analysis.get("specialty", "general"),
            "clinical_reasoning": f"Text analysis identified {len(symptoms)} relevant symptoms",
            "differential_diagnosis": self._text_based_diagnosis(symptoms),
            "recommended_actions": text_analysis.get("recommendations", []),
            "risk_factors": self._text_risk_factors(patient_data, symptoms),
            "follow_up": "Clinical evaluation recommended based on symptom analysis"
        }
    
    def _text_based_diagnosis(self, symptoms: List[Dict]) -> List[str]:
        """Generate diagnosis based on text symptoms"""
        diagnoses = []
        symptom_categories = [s.get("category") for s in symptoms]
        
        if "fever" in symptom_categories and "pain" in symptom_categories:
            diagnoses.append("Inflammatory condition")
        
        if "breathing" in symptom_categories:
            diagnoses.append("Respiratory disorder")
        
        if "nausea" in symptom_categories:
            diagnoses.append("Gastrointestinal condition")
        
        return diagnoses if diagnoses else ["Symptomatic condition requiring evaluation"]
    
    def _text_risk_factors(self, patient_data: Dict, symptoms: List[Dict]) -> List[str]:
        """Identify risk factors from text analysis"""
        risk_factors = []
        
        if any(s.get("severity") == "severe" for s in symptoms):
            risk_factors.append("Severe symptom presentation")
        
        if len(symptoms) > 3:
            risk_factors.append("Multiple concurrent symptoms")
        
        return risk_factors


class MedicalImageModel:
    """Handles image-only medical analysis"""
    
    def analyze_medical_images(self, patient_data: Dict[str, Any], 
                              image_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze using image-only AI model"""
        
        risk_level = image_analysis.get("overall_risk_level", 2)
        findings = image_analysis.get("findings", [])
        
        return {
            "timestamp": datetime.now().isoformat(),
            "model_version": "image_medical_v1.0",
            "priority": risk_level,
            "confidence": 0.8,
            "specialty": image_analysis.get("specialty", "radiology"),
            "clinical_reasoning": f"Imaging analysis revealed {len(findings)} significant findings",
            "differential_diagnosis": self._image_based_diagnosis(findings),
            "recommended_actions": ["Radiological consultation", "Clinical correlation"],
            "risk_factors": self._image_risk_factors(findings),
            "follow_up": "Specialist consultation based on imaging findings"
        }
    
    def _image_based_diagnosis(self, findings: List[Dict]) -> List[str]:
        """Generate diagnosis based on image findings"""
        diagnoses = []
        
        for finding in findings:
            finding_type = finding.get("type", "").lower()
            if "fracture" in finding_type:
                diagnoses.append("Bone fracture")
            elif "lesion" in finding_type:
                diagnoses.append("Space-occupying lesion")
            elif "opacity" in finding_type:
                diagnoses.append("Pulmonary pathology")
        
        return diagnoses if diagnoses else ["Imaging abnormality requiring correlation"]
    
    def _image_risk_factors(self, findings: List[Dict]) -> List[str]:
        """Identify risk factors from image findings"""
        risk_factors = []
        
        if len(findings) > 2:
            risk_factors.append("Multiple imaging abnormalities")
        
        for finding in findings:
            if finding.get("significance") == "high":
                risk_factors.append("High-significance imaging finding")
        
        return risk_factors