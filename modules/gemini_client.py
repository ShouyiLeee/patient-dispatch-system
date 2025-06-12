"""
Client giả lập Gemini Flash 2.0 cho demo hệ thống điều phối bệnh nhân
"""
class GeminiClient:
    def generate(self, prompt, function_call=None):
        # Trả về kết quả mô phỏng dựa trên prompt
        # Ở bản thực tế sẽ gọi API Gemini, ở đây chỉ trả về mẫu
        if function_call == "hospital_matching":
            return {"hospital_list": [
                {"id": "HOSP001", "ten": "Bệnh viện Đa khoa Trung tâm", "khoang_cach": 2.1},
                {"id": "HOSP002", "ten": "Bệnh viện Tim mạch", "khoang_cach": 3.5}
            ]}
        if function_call == "dispatch_matching":
            return {"dispatch_list": [
                {"id": "AMB001", "loai": "Cấp cứu", "khoang_cach": 1.2},
                {"id": "AMB002", "loai": "Vận chuyển thường", "khoang_cach": 2.8}
            ]}
        # Trường hợp QA hoặc text/image
        return {
            "symptoms": ["sốt", "ho"],
            "onset_time": "2 ngày trước",
            "priority": 3,
            "specialty": "hô hấp",
            "findings": ["Tổn thương phổi nhẹ"],
            "risk_level": 2,
            "answer": "Đây là câu trả lời mẫu từ Gemini Flash 2.0."
        }

    def generate_image(self, prompt, image_bytes):
        # Trả về kết quả mô phỏng cho ảnh
        return {
            "findings": ["Tổn thương phổi nhẹ"],
            "risk_level": 2
        }
