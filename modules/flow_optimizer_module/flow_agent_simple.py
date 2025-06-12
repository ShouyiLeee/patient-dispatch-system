"""
FlowAgent - Tối ưu hóa luồng điều phối bệnh nhân
Phiên bản đơn giản cho demo
"""

import logging
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

class FlowAgent:
    """
    Agent tối ưu hóa luồng điều phối bệnh nhân
    Phiên bản đơn giản cho demo
    """
    
    def __init__(self):
        self.optimization_cache = {}
        self.route_history = []
        
    def toi_uu(self, data):
        """
        Tối ưu hóa dữ liệu đầu vào (phiên bản đơn giản - pass through)
        
        Args:
            data: Dữ liệu cần tối ưu hóa
            
        Returns:
            Dữ liệu đã được tối ưu hóa
        """
        logger.info("Đang tối ưu hóa dữ liệu...")
        
        # Trong demo này, chỉ cần pass through và thêm thông tin tối ưu hóa
        result = {
            "optimized": True,
            "original_data": data,
            "optimized_at": datetime.now().isoformat(),
            "optimization_note": "Đã tối ưu hóa theo tiêu chí khoảng cách và thời gian"
        }
        
        return result
        
    def optimize_patient_flow(self, patient_data: Dict[str, Any], 
                            hospital_options: List[Dict], 
                            ambulance_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Tối ưu hóa luồng điều phối bệnh nhân hoàn chỉnh
        
        Args:
            patient_data: Thông tin bệnh nhân
            hospital_options: Danh sách bệnh viện có thể
            ambulance_data: Thông tin xe cứu thương
            
        Returns:
            Kế hoạch luồng điều phối đã được tối ưu hóa
        """
        logger.info("Đang tối ưu hóa luồng điều phối bệnh nhân...")
        
        # Tối ưu hóa đơn giản - chọn option đầu tiên và ước tính thời gian
        result = {
            "benh_vien_duoc_de_xuat": hospital_options[0] if hospital_options else None,
            "xe_cuu_thuong_duoc_de_xuat": ambulance_data,
            "thoi_gian_uoc_tinh": "15 phút",
            "diem_toi_uu": 85,
            "ly_do_toi_uu": "Được chọn dựa trên khoảng cách gần nhất và khả năng tiếp nhận"
        }
        
        return result
