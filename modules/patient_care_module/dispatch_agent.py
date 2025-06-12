"""
Dispatch Agent - Finds suitable ambulances with paramedic availability
"""
import random
from typing import Dict, Any, List
from modules.gemini_client import GeminiClient

class DispatchAgent:
    def __init__(self, gemini_client=None):
        self.gemini = gemini_client or GeminiClient()
        self.mock_ambulances = self._generate_mock_ambulances()
    
    def _generate_mock_ambulances(self) -> List[Dict[str, Any]]:
        """Generate mock ambulance data with paramedic availability"""
        paramedics = [
            "Nguyễn Văn Anh", "Trần Thị Bình", "Lê Văn Cường", 
            "Phạm Thị Dung", "Hoàng Văn Em", "Vũ Thị Phương",
            "Đặng Văn Giang", "Ngô Thị Hương", "Bùi Văn Inh",
            "Lý Thị Khánh", "Phan Văn Long", "Mai Thị Minh"
        ]
        
        ambulances = [
            {
                "type": "Xe cấp cứu loại A",
                "vehicle_id": "CC01",
                "distance": 1.2,
                "equipment": ["máy thở", "máy sốc tim", "bộ truyền dịch"],
                "available": True,
                "capacity": "1 bệnh nhân nặng"
            },
            {
                "type": "Xe cấp cứu loại B", 
                "vehicle_id": "CC02",
                "distance": 2.8,
                "equipment": ["máy đo huyết áp", "bộ sơ cứu", "bình oxy"],
                "available": True,
                "capacity": "2 bệnh nhân nhẹ"
            },
            {
                "type": "Xe cấp cứu loại A",
                "vehicle_id": "CC03", 
                "distance": 1.8,
                "equipment": ["máy thở", "máy sốc tim", "bộ truyền dịch", "thuốc cấp cứu"],
                "available": True,
                "capacity": "1 bệnh nhân nặng"
            },
            {
                "type": "Xe cấp cứu nhi",
                "vehicle_id": "CC04",
                "distance": 3.5,
                "equipment": ["thiết bị nhi khoa", "máy thở trẻ em", "bộ sơ cứu nhi"],
                "available": True,
                "capacity": "trẻ em và sơ sinh"
            },
            {
                "type": "Xe cấp cứu đặc biệt",
                "vehicle_id": "CC05",
                "distance": 4.2,
                "equipment": ["máy ECMO", "máy thở cao cấp", "thiết bị hồi sức"],
                "available": False,  # Currently busy
                "capacity": "1 bệnh nhân rất nặng"
            }
        ]
        
        # Assign paramedics to available ambulances
        available_paramedics = paramedics.copy()
        for ambulance in ambulances:
            if ambulance["available"] and available_paramedics:
                # Assign 1-2 paramedics per ambulance
                num_paramedics = 2 if ambulance["type"] in ["Xe cấp cứu loại A", "Xe cấp cứu đặc biệt"] else 1
                assigned = []
                for _ in range(min(num_paramedics, len(available_paramedics))):
                    paramedic = available_paramedics.pop(random.randint(0, len(available_paramedics)-1))
                    assigned.append(paramedic)
                ambulance["paramedic"] = ", ".join(assigned) if len(assigned) > 1 else assigned[0] if assigned else "Đang điều động"
            else:
                ambulance["paramedic"] = "Không khả dụng"
        
        return ambulances
    
    def tim_xe_cuu_thuong(self, patient_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Find suitable ambulances for patient
        
        Args:
            patient_info: Patient information dictionary
            
        Returns:
            List of suitable ambulances with paramedic availability
        """
        try:
            # Get patient requirements
            is_emergency = patient_info.get('is_emergency', False)
            priority = patient_info.get('muc_do_uu_tien', patient_info.get('priority_level', 3))
            specialty = patient_info.get('chuyen_khoa', patient_info.get('specialty', 'nội khoa'))
            
            suitable_ambulances = []
            
            for ambulance in self.mock_ambulances:
                # Skip unavailable ambulances
                if not ambulance["available"]:
                    continue
                
                # For emergency cases, prioritize type A ambulances
                if is_emergency and priority >= 5:
                    if "loại A" not in ambulance["type"] and "đặc biệt" not in ambulance["type"]:
                        continue
                
                # For pediatric cases, prefer pediatric ambulance
                if specialty == "nhi khoa":
                    if "nhi" in ambulance["type"]:
                        ambulance["priority_score"] = 1  # Highest priority
                    else:
                        ambulance["priority_score"] = 3
                else:
                    if "nhi" in ambulance["type"]:
                        ambulance["priority_score"] = 4  # Lower priority for non-pediatric
                    else:
                        ambulance["priority_score"] = 2
                
                # Calculate ETA based on distance
                eta_minutes = int(ambulance["distance"] * 2.5)  # Assume 2.5 minutes per km
                
                ambulance_info = {
                    "type": ambulance["type"],
                    "vehicle_id": ambulance["vehicle_id"],
                    "distance": ambulance["distance"],
                    "eta_minutes": eta_minutes,
                    "paramedic": ambulance["paramedic"],
                    "equipment": ambulance["equipment"],
                    "capacity": ambulance["capacity"],
                    "available": True,
                    "priority_score": ambulance.get("priority_score", 2)
                }
                
                suitable_ambulances.append(ambulance_info)
            
            # Sort by priority score, then by distance
            suitable_ambulances.sort(key=lambda x: (x["priority_score"], x["distance"]))
            
            return suitable_ambulances[:3]  # Return top 3
            
        except Exception as e:
            # Return mock data on error
            return [{
                "type": "Xe cấp cứu loại A",
                "vehicle_id": "CC01",
                "distance": 1.5,
                "eta_minutes": 4,
                "paramedic": "Nguyễn Văn Anh",
                "equipment": ["máy thở", "máy sốc tim"],
                "capacity": "1 bệnh nhân nặng",
                "available": True,
                "error": str(e)
            }]
