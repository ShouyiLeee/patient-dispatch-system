"""
Medical QA Chatbot using Gemini Flash 2.0
English function names with Vietnamese data support
"""

import logging
from modules.gemini_client import GeminiClient

logger = logging.getLogger(__name__)

class QAChatbot:
    def __init__(self, gemini_client=None):
        self.gemini = gemini_client or GeminiClient()
        
    def ask_question(self, question, context=None):
        """
        Ask a medical question and get response
        
        Args:
            question: Medical question in Vietnamese
            context: Additional context for the question
            
        Returns:
            Dictionary with response
        """
        try:
            prompt = f"""Hỏi đáp y tế: {question}
            
Hãy trả lời một cách chuyên nghiệp và hữu ích bằng tiếng Việt.
Nếu câu hỏi liên quan đến triệu chứng nghiêm trọng, hãy khuyên bệnh nhân đi khám ngay."""
            
            if context:
                prompt += f"\nBối cảnh: {context}"
                
            response = self.gemini.generate(prompt)
            
            return {
                "success": True,
                "answer": response.get("answer", "Xin lỗi, tôi chưa có câu trả lời cho câu hỏi này."),
                "context": context
            }
            
        except Exception as e:
            logger.error(f"Error in QA chatbot: {e}")
            return {
                "success": False,
                "answer": "Xin lỗi, hệ thống đang gặp lỗi. Vui lòng thử lại sau.",
                "error": str(e)
            }
    
    def hoi_dap(self, cau_hoi, context=None):
        """Vietnamese wrapper for compatibility"""
        return self.ask_question(cau_hoi, context)
