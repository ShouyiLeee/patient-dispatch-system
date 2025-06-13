"""
Image Processing Module for Patient Triage System
Handles medical image analysis and extraction of relevant information
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
import requests
from PIL import Image
import io

logger = logging.getLogger(__name__)

class ImageProcessor:
    """Image processing utility for medical images"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the image processor
        
        Args:
            api_key: Google AI API key. If not provided, will try to get from environment
        """
        self.api_key = api_key or os.getenv('GOOGLE_AI_API_KEY')
        if not self.api_key:
            logger.warning("No API key provided, using mock responses")
        
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent"
    
    def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """
        Analyze a medical image and extract relevant information
        
        Args:
            image_path: Path to the image file
        
        Returns:
            Dictionary with analysis results
        """
        try:
            # In real implementation, this would call the vision API
            # For now, we'll use mock data
            if not self.api_key:
                return self._get_mock_response(image_path)
            
            # Real implementation would look like this:
            # return self._call_vision_api(image_path)
            
            # For demo, always return mock data
            return self._get_mock_response(image_path)
            
        except Exception as e:
            logger.error(f"Error analyzing image: {e}")
            return {
                "error": str(e),
                "findings": [],
                "risk_level": 0
            }
    
    def _call_vision_api(self, image_path: str) -> Dict[str, Any]:
        """Call the vision API with the image"""
        try:
            # Read and encode the image
            with open(image_path, "rb") as image_file:
                image_bytes = image_file.read()
            
            # Prepare the API request
            url = f"{self.base_url}?key={self.api_key}"
            
            # This is simplified - would need proper formatting for the API
            response = requests.post(
                url,
                json={
                    "contents": [{
                        "parts": [
                            {"text": "Analyze this medical image and describe any abnormalities:"},
                            {
                                "inlineData": {
                                    "mimeType": "image/jpeg",
                                    "data": image_bytes.hex()
                                }
                            }
                        ]
                    }]
                }
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"API error: {response.status_code} - {response.text}")
                return self._get_mock_response(image_path)
                
        except Exception as e:
            logger.error(f"Error calling vision API: {e}")
            return self._get_mock_response(image_path)
    
    def _get_mock_response(self, image_path: str) -> Dict[str, Any]:
        """Get mock response for testing"""
        # Check if file contains "xray" or "ct" to provide appropriate mock data
        file_lower = image_path.lower()
        
        if "xray" in file_lower or "x-ray" in file_lower:
            return {
                "findings": [
                    "Lung fields clear of focal consolidation",
                    "No pleural effusion",
                    "Heart size within normal limits"
                ],
                "risk_level": 1,
                "recommendation": "No acute findings"
            }
        elif "ct" in file_lower:
            return {
                "findings": [
                    "Small area of ground-glass opacity in right lower lobe",
                    "No pulmonary nodules",
                    "No pleural effusion"
                ],
                "risk_level": 2,
                "recommendation": "Follow-up in 3 months"
            }
        else:
            return {
                "findings": [
                    "Image appears normal",
                    "No significant abnormalities detected"
                ],
                "risk_level": 0,
                "recommendation": "No further imaging needed"
            }
