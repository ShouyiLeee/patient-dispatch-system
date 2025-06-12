"""
FlowAgent - Optimizes routing based on load and traffic
Phiên bản đơn giản cho demo hệ thống điều phối bệnh nhân
"""

import logging
from typing import Dict, Any, List
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class FlowAgent:
    """
    Agent tối ưu hóa luồng bệnh nhân
    Phiên bản đơn giản để demo, có thể mở rộng với AI model phức tạp hơn
    """
    
    def __init__(self):
        logger.info("Khởi tạo FlowAgent")
    
    def toi_uu(self, danh_sach_input):
        """
        Hàm tối ưu hóa đơn giản cho demo
        
        Args:
            danh_sach_input: Danh sách cần tối ưu (bệnh viện, xe cứu thương, etc.)
            
        Returns:
            Dict: Kết quả tối ưu hóa
        """
        logger.info("Đang thực hiện tối ưu hóa...")
        
        try:
            # Nếu là danh sách bệnh viện
            if isinstance(danh_sach_input, list) and danh_sach_input:
                # Kiểm tra xem có phải danh sách bệnh viện không
                if all(isinstance(item, dict) and 'ten' in item for item in danh_sach_input):
                    return self._toi_uu_benh_vien(danh_sach_input)
                # Kiểm tra danh sách xe cứu thương
                elif all(isinstance(item, dict) and 'loai' in item for item in danh_sach_input):
                    return self._toi_uu_xe_cuu_thuong(danh_sach_input)
            
            # Trường hợp khác - chỉ trả về input
            return {
                "du_lieu_goc": danh_sach_input,
                "trang_thai": "khong_can_toi_uu",
                "thoi_gian": datetime.now().isoformat(),
                "thong_bao": "Dữ liệu không cần tối ưu hóa"
            }
            
        except Exception as e:
            logger.error(f"Lỗi tối ưu hóa: {e}")
            return {
                "loi": str(e),
                "du_lieu_goc": danh_sach_input,
                "thoi_gian": datetime.now().isoformat()
            }
    
    def _toi_uu_benh_vien(self, danh_sach_benh_vien: List[Dict]) -> Dict:
        """Tối ưu hóa danh sách bệnh viện"""
        logger.info("Tối ưu hóa danh sách bệnh viện...")
        
        # Sắp xếp theo khoảng cách và điểm ưu tiên
        def tinh_diem_uu_tien(benh_vien):
            khoang_cach = benh_vien.get('khoang_cach', 999)
            # Điểm càng thấp càng tốt (khoảng cách gần)
            diem = khoang_cach
            
            # Thưởng điểm cho bệnh viện có ID đặc biệt (bệnh viện lớn)
            if 'HOSP001' in benh_vien.get('id', ''):
                diem -= 1  # Ưu tiên cao hơn
                
            return diem
        
        danh_sach_sap_xep = sorted(
            danh_sach_benh_vien,
            key=tinh_diem_uu_tien
        )
        
        return {
            "loai": "toi_uu_benh_vien",
            "danh_sach_toi_uu": danh_sach_sap_xep,
            "benh_vien_tot_nhat": danh_sach_sap_xep[0] if danh_sach_sap_xep else None,
            "ly_do": "Đã sắp xếp theo khoảng cách và độ ưu tiên",
            "so_luong": len(danh_sach_sap_xep),
            "thoi_gian_toi_uu": datetime.now().isoformat()
        }
    
    def _toi_uu_xe_cuu_thuong(self, danh_sach_xe: List[Dict]) -> Dict:
        """Tối ưu hóa danh sách xe cứu thương"""
        logger.info("Tối ưu hóa danh sách xe cứu thương...")
        
        # Sắp xếp theo khoảng cách và loại xe
        def tinh_diem_xe(xe):
            khoang_cach = xe.get('khoang_cach', 999)
            diem = khoang_cach
            
            # Ưu tiên xe cấp cứu hơn xe vận chuyển thường
            if 'Cấp cứu' in xe.get('loai', ''):
                diem -= 0.5
                
            return diem
        
        danh_sach_sap_xep = sorted(
            danh_sach_xe,
            key=tinh_diem_xe
        )
        
        return {
            "loai": "toi_uu_xe_cuu_thuong",
            "danh_sach_toi_uu": danh_sach_sap_xep,
            "xe_tot_nhat": danh_sach_sap_xep[0] if danh_sach_sap_xep else None,
            "ly_do": "Đã sắp xếp theo khoảng cách và loại xe",
            "so_luong": len(danh_sach_sap_xep),
            "thoi_gian_toi_uu": datetime.now().isoformat()
        }
