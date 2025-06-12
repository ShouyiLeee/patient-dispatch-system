"""
Hospital Agent - Finds suitable hospitals with doctor availability
English function names with Vietnamese data only
"""
import random
from typing import Dict, Any, List
from modules.gemini_client import GeminiClient

class HospitalAgent:
    def __init__(self, gemini_client=None):
        self.gemini = gemini_client or GeminiClient()
        self.mock_hospitals = self._generate_mock_hospitals()
    
    def _generate_mock_hospitals(self) -> List[Dict[str, Any]]:
        """Generate mock hospital data with doctor availability"""
        doctors_by_specialty = {
            "nội khoa": ["BS. Nguyễn Văn A", "BS. Trần Thị B", "BS. Lê Văn C"],
            "ngoại khoa": ["BS. Phạm Văn D", "BS. Hoàng Thị E", "BS. Vũ Văn F"],
            "tim mạch": ["BS. Đặng Văn G", "BS. Ngô Thị H", "BS. Bùi Văn I"],
            "cấp cứu": ["BS. Lý Văn J", "BS. Phan Thị K", "BS. Dương Văn L"],
            "nhi khoa": ["BS. Mai Thị M", "BS. Trương Văn N", "BS. Đinh Thị O"],
            "sản phụ khoa": ["BS. Cao Thị P", "BS. Võ Văn Q", "BS. Hồ Thị R"]
        }
        
        hospitals = [
            {
                "name": "Bệnh viện Chợ Rẫy",
                "distance": 2.5,
                "specialty": ["nội khoa", "ngoại khoa", "tim mạch", "cấp cứu"],
                "available": True,
                "capacity": 80,
                "current_load": 65
            },
            {
                "name": "Bệnh viện Đại học Y Dược",
                "distance": 3.2,
                "specialty": ["nội khoa", "tim mạch", "nhi khoa"],
                "available": True,
                "capacity": 120,
                "current_load": 90
            },
            {
                "name": "Bệnh viện Thống Nhất",
                "distance": 1.8,
                "specialty": ["nội khoa", "ngoại khoa", "cấp cứu"],
                "available": True,
                "capacity": 60,
                "current_load": 45
            },
            {
                "name": "Bệnh viện Từ Dũ",
                "distance": 4.1,
                "specialty": ["sản phụ khoa", "nhi khoa"],
                "available": True,
                "capacity": 40,
                "current_load": 25
            },
            {
                "name": "Bệnh viện Nhi Đồng 1",
                "distance": 3.8,
                "specialty": ["nhi khoa", "cấp cứu"],
                "available": True,
                "capacity": 50,
                "current_load": 30
            }
        ]
        
        # Add available doctors to each hospital
        for hospital in hospitals:
            hospital["available_doctors"] = []
            for specialty in hospital["specialty"]:
                available_docs = doctors_by_specialty.get(specialty, [])
                if available_docs:
                    # Randomly assign 1-2 available doctors per specialty
                    num_docs = random.randint(1, min(2, len(available_docs)))
                    selected_docs = random.sample(available_docs, num_docs)
                    for doc in selected_docs:
                        hospital["available_doctors"].append({
                            "name": doc,
                            "specialty": specialty,
                            "available": random.choice([True, True, False])  # 2/3 chance available
                        })
        
        return hospitals
    
    def tim_benh_vien(self, patient_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Find suitable hospitals for patient
        
        Args:
            patient_info: Patient information dictionary
            
        Returns:
            List of suitable hospitals with doctor availability
        """
        try:
            # Get patient requirements
            required_specialty = patient_info.get('chuyen_khoa', patient_info.get('specialty', 'nội khoa'))
            is_emergency = patient_info.get('is_emergency', False)
            priority = patient_info.get('muc_do_uu_tien', patient_info.get('priority_level', 3))
            
            suitable_hospitals = []
            
            for hospital in self.mock_hospitals:
                # Check if hospital has required specialty
                if required_specialty not in hospital["specialty"]:
                    continue
                
                # Check availability
                if not hospital["available"]:
                    continue
                
                # Check capacity (emergency cases get priority)
                load_percentage = (hospital["current_load"] / hospital["capacity"]) * 100
                if not is_emergency and load_percentage > 85:
                    continue
                
                # Find available doctor for specialty
                available_doctor = None
                for doc in hospital["available_doctors"]:
                    if doc["specialty"] == required_specialty and doc["available"]:
                        available_doctor = doc["name"]
                        break
                
                # If no doctor available, skip (unless emergency)
                if not available_doctor and not is_emergency:
                    continue
                
                # Add hospital to suitable list
                hospital_info = {
                    "name": hospital["name"],
                    "distance": hospital["distance"],
                    "specialty": required_specialty,
                    "available_doctor": available_doctor or "BS. Trực cấp cứu",
                    "emergency_doctor": "BS. Trực cấp cứu" if is_emergency else available_doctor,
                    "capacity_status": f"{hospital['current_load']}/{hospital['capacity']}",
                    "load_percentage": load_percentage,
                    "estimated_wait_time": max(5, int(load_percentage / 5)),  # minutes
                    "available": True
                }
                
                suitable_hospitals.append(hospital_info)
            
            # Sort by distance for emergency, by wait time for regular
            if is_emergency:
                suitable_hospitals.sort(key=lambda x: x["distance"])
            else:
                suitable_hospitals.sort(key=lambda x: (x["estimated_wait_time"], x["distance"]))
            
            return suitable_hospitals[:5]  # Return top 5
            
        except Exception as e:
            # Return mock data on error
            return [{
                "name": "Bệnh viện Chợ Rẫy",
                "distance": 2.5,
                "specialty": required_specialty,
                "available_doctor": "BS. Nguyễn Văn A",
                "emergency_doctor": "BS. Trực cấp cứu",
                "capacity_status": "65/80",
                "load_percentage": 81,
                "estimated_wait_time": 15,
                "available": True,
                "error": str(e)
            }]
    
    def find_hospitals(self, patient_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Find suitable hospitals for patient (English method name)
        
        Args:
            patient_info: Patient information dictionary
            
        Returns:
            List of suitable hospitals with doctor availability
        """
        return self.tim_benh_vien(patient_info)
