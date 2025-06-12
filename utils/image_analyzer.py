import os
import base64
import requests
import json
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ImageAnalyzer:
    """
    Image analyzer using Google Gemini Flash 2.0 API for medical image analysis
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the image analyzer
        
        Args:
            api_key: Google AI API key. If not provided, will try to get from environment
        """
        self.api_key = api_key or os.getenv('GOOGLE_AI_API_KEY')
        if not self.api_key:
            logger.warning("No Google AI API key provided. Image analysis will be disabled.")
        
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"
    
    def analyze_medical_image(self, image_data: bytes, mime_type: str = "image/jpeg") -> Dict[str, Any]:
        """
        Analyze medical image using Gemini Flash 2.0
        
        Args:
            image_data: Raw image data in bytes
            mime_type: MIME type of the image
            
        Returns:
            Dict containing analysis results
        """
        if not self.api_key:
            return {
                "success": False,
                "error": "API key not configured"
            }
        
        try:
            # Convert image to base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # Prepare the request payload
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": self._get_medical_analysis_prompt()
                            },
                            {
                                "inline_data": {
                                    "mime_type": mime_type,
                                    "data": image_base64
                                }
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.3,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 1024,
                }
            }
            
            # Make API request
            headers = {
                "Content-Type": "application/json"
            }
            
            url = f"{self.base_url}?key={self.api_key}"
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                if 'candidates' in result and len(result['candidates']) > 0:
                    analysis_text = result['candidates'][0]['content']['parts'][0]['text']
                    
                    # Parse the structured response
                    parsed_result = self._parse_analysis_response(analysis_text)
                    
                    return {
                        "success": True,
                        "analysis": parsed_result.get("formatted_analysis", analysis_text),
                        "risk_level": parsed_result.get("risk_level", "unknown"),
                        "suggested_description": parsed_result.get("suggested_description", ""),
                        "emergency_indicators": parsed_result.get("emergency_indicators", []),
                        "raw_response": analysis_text
                    }
                else:
                    return {
                        "success": False,
                        "error": "No analysis generated"
                    }
            else:
                error_detail = response.text
                logger.error(f"Gemini API error: {response.status_code} - {error_detail}")
                return {
                    "success": False,
                    "error": f"API request failed: {response.status_code}"
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Request timeout"
            }
        except Exception as e:
            logger.error(f"Error analyzing image: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _get_medical_analysis_prompt(self) -> str:
        """
        Get the prompt for medical image analysis
        """
        return """
        Bạn là một chuyên gia y tế AI. Hãy phân tích hình ảnh y tế này và cung cấp thông tin theo định dạng sau:

        PHÂN TÍCH HÌNH ẢNH Y TẾ:
        
        **Mô tả quan sát:**
        - [Mô tả chi tiết những gì thấy trong hình ảnh]
        
        **Mức độ rủi ro:**
        - [THẤP/TRUNG BÌNH/CAO/RẤT CAO]
        
        **Các dấu hiệu đáng lo ngại:**
        - [Liệt kê các dấu hiệu cần chú ý, nếu có]
        
        **Khuyến nghị sơ bộ:**
        - [Đưa ra khuyến nghị về việc cần khám bác sĩ hay không]
        
        **Mô tả triệu chứng gợi ý:**
        [Đưa ra mô tả ngắn gọn có thể dùng để điền vào form]
        
        **LƯU Ý QUAN TRỌNG:**
        - Đây chỉ là phân tích sơ bộ, không thay thế chẩn đoán y tế chuyên nghiệp
        - Nếu có dấu hiệu nghiêm trọng, khuyến nghị đến bệnh viện ngay lập tức
        
        Hãy phân tích một cách khách quan và cẩn thận, tránh đưa ra chẩn đoán chắc chắn.
        """
    
    def _parse_analysis_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse the structured response from Gemini
        
        Args:
            response_text: Raw response text from Gemini
            
        Returns:
            Parsed analysis data
        """
        try:
            # Extract risk level
            risk_level = "unknown"
            if "RẤT CAO" in response_text.upper():
                risk_level = "very_high"
            elif "CAO" in response_text.upper():
                risk_level = "high"
            elif "TRUNG BÌNH" in response_text.upper():
                risk_level = "medium"
            elif "THẤP" in response_text.upper():
                risk_level = "low"
            
            # Extract suggested description (look for the section after "Mô tả triệu chứng gợi ý:")
            suggested_description = ""
            lines = response_text.split('\n')
            capture_description = False
            for line in lines:
                if "mô tả triệu chứng gợi ý" in line.lower():
                    capture_description = True
                    continue
                elif capture_description and line.strip():
                    if line.startswith('**') or line.startswith('LƯU Ý'):
                        break
                    suggested_description += line.strip() + " "
            
            # Format the analysis for display
            formatted_analysis = self._format_analysis_for_display(response_text)
            
            # Extract emergency indicators
            emergency_indicators = []
            if any(keyword in response_text.upper() for keyword in 
                   ["NGAY LẬP TỨC", "CẤP CỨU", "KHẨN CẤP", "RẤT CAO", "NGHIÊM TRỌNG"]):
                emergency_indicators.append("Cần xử lý khẩn cấp")
            
            return {
                "risk_level": risk_level,
                "suggested_description": suggested_description.strip(),
                "emergency_indicators": emergency_indicators,
                "formatted_analysis": formatted_analysis
            }
            
        except Exception as e:
            logger.error(f"Error parsing analysis response: {str(e)}")
            return {
                "risk_level": "unknown",
                "suggested_description": "",
                "emergency_indicators": [],
                "formatted_analysis": response_text
            }
    
    def _format_analysis_for_display(self, text: str) -> str:
        """
        Format the analysis text for better display in the UI
        """
        # Convert markdown-like formatting to HTML
        formatted = text.replace('**', '<strong>').replace('**', '</strong>')
        
        # Convert bullet points
        lines = formatted.split('\n')
        html_lines = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('-'):
                html_lines.append(f"<li>{line[1:].strip()}</li>")
            elif line.startswith('**') and line.endswith('**'):
                html_lines.append(f"<h6 class='mt-3'>{line[2:-2]}</h6>")
            elif line:
                html_lines.append(f"<p>{line}</p>")
        
        return '\n'.join(html_lines)

# Create a global instance
image_analyzer = ImageAnalyzer()
