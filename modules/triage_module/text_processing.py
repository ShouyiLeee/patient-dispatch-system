"""
Xử lý văn bản trong phân luồng bệnh nhân - sử dụng Gemini Flash 2.0
"""
from modules.gemini_client import GeminiClient

class TextProcessor:
    def __init__(self, gemini_client=None):
        self.gemini = gemini_client or GeminiClient()

    def phan_tich(self, noi_dung_benh_nhan, thong_tin_bo_sung=None):
        prompt = f"Hãy trích xuất triệu chứng, thời gian khởi phát, mức độ ưu tiên, chuyên khoa phù hợp từ mô tả sau: {noi_dung_benh_nhan}"
        if thong_tin_bo_sung:
            prompt += f"\nThông tin bổ sung: {thong_tin_bo_sung}"
        ket_qua = self.gemini.generate(prompt)
        return {
            "trieu_chung": ket_qua.get("symptoms", []),
            "thoi_gian_khoi_phat": ket_qua.get("onset_time", ""),
            "muc_do_uu_tien": ket_qua.get("priority", 2),
            "chuyen_khoa": ket_qua.get("specialty", "chung"),
            "raw": ket_qua
        }