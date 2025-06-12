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
        
    def initialize_models(self):
        """Initialize traffic and hospital load models"""    def toi_uu(self, data):
        """
        Tối ưu hóa dữ liệu đầu vào (phiên bản đơn giản - pass through)
        
        Args:
            data: Dữ liệu cần tối ưu hóa
            
        Returns:
            Dữ liệu đã được tối ưu hóa (trong demo này chỉ là pass through)
        """
        logger.info("Tối ưu hóa dữ liệu...")
        return {
            "optimized": True,
            "original_data": data,
            "optimized_at": datetime.now().isoformat()
        }
    
    def optimize_patient_flow(self, patient_data: Dict[str, Any], 
                            hospital_options: List[Dict], 
                            ambulance_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize complete patient flow including routing and hospital selection
        
        Args:
            patient_data: Patient information including location and priority
            hospital_options: List of available hospitals
            ambulance_data: Ambulance location and type
            
        Returns:
            Optimized flow plan with routes and timing
        """
        if not all([self.traffic_model, self.hospital_load_estimator]):
            self.initialize_models()
            
        optimization_id = f"OPT_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        flow_plan = {
            "optimization_id": optimization_id,
            "timestamp": datetime.now().isoformat(),
            "patient_id": patient_data.get("patient_id"),
            "optimal_hospital": None,
            "optimal_route": None,
            "estimated_total_time": None,
            "optimization_factors": [],
            "alternative_options": []
        }
        
        try:
            logger.info(f"Optimizing patient flow for patient {patient_data.get('patient_id')}")
            
            patient_location = (
                patient_data.get("latitude", 10.7743),
                patient_data.get("longitude", 106.6675)
            )
            
            ambulance_location = (
                ambulance_data.get("latitude", 10.7743),
                ambulance_data.get("longitude", 106.6675)
            )
            
            priority = patient_data.get("priority", 2)
            
            # Evaluate each hospital option
            hospital_evaluations = []
            
            for hospital in hospital_options:
                evaluation = self._evaluate_hospital_option(
                    patient_location,
                    ambulance_location,
                    hospital,
                    priority,
                    patient_data
                )
                hospital_evaluations.append(evaluation)
            
            # Sort by optimization score
            hospital_evaluations.sort(key=lambda x: x["optimization_score"], reverse=True)
            
            if hospital_evaluations:
                flow_plan["optimal_hospital"] = hospital_evaluations[0]
                flow_plan["alternative_options"] = hospital_evaluations[1:3]  # Top 3 alternatives
                
                # Generate optimal route
                optimal_route = self._generate_optimal_route(
                    ambulance_location,
                    patient_location,
                    hospital_evaluations[0]["hospital_location"],
                    priority
                )
                
                flow_plan["optimal_route"] = optimal_route
                flow_plan["estimated_total_time"] = optimal_route["total_time_minutes"]
                flow_plan["optimization_factors"] = self._get_optimization_factors(hospital_evaluations[0])
                
                # Cache optimization result
                self.optimization_cache[optimization_id] = flow_plan
                
                # Add to route history
                self.route_history.append({
                    "optimization_id": optimization_id,
                    "timestamp": datetime.now(),
                    "patient_priority": priority,
                    "selected_hospital": hospital_evaluations[0]["hospital_id"],
                    "total_time": optimal_route["total_time_minutes"]
                })
                
                logger.info(f"Flow optimization completed - Selected: {hospital_evaluations[0]['hospital_name']}")
                
            else:
                flow_plan["error"] = "No suitable hospitals found for optimization"
                
        except Exception as e:
            logger.error(f"Flow optimization failed: {e}")
            flow_plan["error"] = str(e)
            
        return flow_plan
    
    def _evaluate_hospital_option(self, patient_location: Tuple[float, float],
                                 ambulance_location: Tuple[float, float],
                                 hospital: Dict[str, Any],
                                 priority: int,
                                 patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate a single hospital option"""
        
        hospital_location = (hospital["location"]["lat"], hospital["location"]["lng"])
        
        evaluation = {
            "hospital_id": hospital["hospital_id"],
            "hospital_name": hospital["hospital_name"],
            "hospital_location": hospital_location,
            "optimization_score": 0.0,
            "factors": {}
        }
        
        try:
            # Factor 1: Travel time (40% weight)
            travel_time = self._calculate_total_travel_time(
                ambulance_location, patient_location, hospital_location, priority
            )
            time_score = self._score_travel_time(travel_time, priority)
            evaluation["factors"]["travel_time"] = {
                "value": travel_time,
                "score": time_score,
                "weight": 0.4
            }
            
            # Factor 2: Hospital load (25% weight)
            hospital_load = self.hospital_load_estimator.estimate_hospital_load(hospital["hospital_id"])
            load_score = self._score_hospital_load(hospital_load)
            evaluation["factors"]["hospital_load"] = {
                "value": hospital_load,
                "score": load_score,
                "weight": 0.25
            }
            
            # Factor 3: Specialty match (20% weight)
            specialty_match = self._evaluate_specialty_match(hospital, patient_data)
            evaluation["factors"]["specialty_match"] = {
                "value": specialty_match,
                "score": specialty_match,
                "weight": 0.2
            }
            
            # Factor 4: Resource availability (15% weight)
            resource_availability = self._evaluate_resource_availability(hospital)
            evaluation["factors"]["resource_availability"] = {
                "value": resource_availability,
                "score": resource_availability,
                "weight": 0.15
            }
            
            # Calculate weighted optimization score
            evaluation["optimization_score"] = (
                time_score * 0.4 +
                load_score * 0.25 +
                specialty_match * 0.2 +
                resource_availability * 0.15
            )
            
            # Priority bonus for emergency cases
            if priority >= 4:
                evaluation["optimization_score"] *= 1.1  # 10% bonus for high priority
            
        except Exception as e:
            logger.error(f"Hospital evaluation failed for {hospital['hospital_id']}: {e}")
            evaluation["error"] = str(e)
            evaluation["optimization_score"] = 0.0
            
        return evaluation
    
    def _calculate_total_travel_time(self, ambulance_location: Tuple[float, float],
                                   patient_location: Tuple[float, float],
                                   hospital_location: Tuple[float, float],
                                   priority: int) -> int:
        """Calculate total travel time: ambulance to patient + patient to hospital"""
        
        # Ambulance to patient
        pickup_time = self.traffic_model.estimate_travel_time(
            ambulance_location, patient_location, priority
        )
        
        # Patient to hospital
        transport_time = self.traffic_model.estimate_travel_time(
            patient_location, hospital_location, priority
        )
        
        # Add loading/preparation time
        preparation_time = 5 if priority >= 4 else 10  # Less prep time for emergencies
        
        return pickup_time + preparation_time + transport_time
    
    def _score_travel_time(self, travel_time: int, priority: int) -> float:
        """Score travel time (lower time = higher score)"""
        if priority >= 4:  # Emergency
            # Critical time thresholds for emergencies
            if travel_time <= 15:
                return 1.0
            elif travel_time <= 25:
                return 0.8
            elif travel_time <= 35:
                return 0.6
            else:
                return 0.3
        else:  # Standard
            # More lenient for non-emergencies
            if travel_time <= 30:
                return 1.0
            elif travel_time <= 45:
                return 0.8
            elif travel_time <= 60:
                return 0.6
            else:
                return 0.4
    
    def _score_hospital_load(self, hospital_load: Dict[str, Any]) -> float:
        """Score hospital load (lower load = higher score)"""
        occupancy_rate = hospital_load.get("occupancy_rate", 0.5)
        emergency_wait_time = hospital_load.get("emergency_wait_time", 15)
        
        # Score based on occupancy
        if occupancy_rate <= 0.7:
            occupancy_score = 1.0
        elif occupancy_rate <= 0.85:
            occupancy_score = 0.7
        else:
            occupancy_score = 0.4
        
        # Score based on wait time
        if emergency_wait_time <= 10:
            wait_score = 1.0
        elif emergency_wait_time <= 20:
            wait_score = 0.8
        else:
            wait_score = 0.5
        
        return (occupancy_score + wait_score) / 2
    
    def _evaluate_specialty_match(self, hospital: Dict[str, Any], patient_data: Dict[str, Any]) -> float:
        """Evaluate how well hospital specialties match patient needs"""
        required_specialty = patient_data.get("required_specialty", "general")
        hospital_specialties = hospital.get("specialties", [])
        
        if required_specialty in hospital_specialties:
            return 1.0
        elif "general" in hospital_specialties or hospital.get("trauma_center", False):
            return 0.7
        else:
            return 0.4
    
    def _evaluate_resource_availability(self, hospital: Dict[str, Any]) -> float:
        """Evaluate hospital resource availability"""
        # Simulated resource evaluation
        # In real implementation, this would check actual bed availability, equipment, staff
        
        bed_availability = hospital.get("bed_availability", 10)
        hospital_type = hospital.get("type", "general")
        
        # Score based on bed availability
        if bed_availability >= 10:
            bed_score = 1.0
        elif bed_availability >= 5:
            bed_score = 0.8
        elif bed_availability >= 1:
            bed_score = 0.6
        else:
            bed_score = 0.2
        
        # Bonus for specialized hospitals
        type_bonus = 1.1 if hospital_type == "specialty" else 1.0
        
        return min(1.0, bed_score * type_bonus)
    
    def _generate_optimal_route(self, ambulance_location: Tuple[float, float],
                              patient_location: Tuple[float, float],
                              hospital_location: Tuple[float, float],
                              priority: int) -> Dict[str, Any]:
        """Generate optimal route with detailed timing and directions"""
        
        route = {
            "route_segments": [],
            "total_distance_km": 0.0,
            "total_time_minutes": 0,
            "traffic_conditions": [],
            "alternative_routes": []
        }
        
        try:
            # Segment 1: Ambulance to patient
            pickup_segment = self.traffic_model.get_route_details(
                ambulance_location, patient_location, priority
            )
            
            # Segment 2: Patient to hospital
            transport_segment = self.traffic_model.get_route_details(
                patient_location, hospital_location, priority
            )
            
            route["route_segments"] = [
                {
                    "segment": "pickup",
                    "from": ambulance_location,
                    "to": patient_location,
                    "distance_km": pickup_segment["distance_km"],
                    "time_minutes": pickup_segment["time_minutes"],
                    "traffic_level": pickup_segment["traffic_level"]
                },
                {
                    "segment": "transport",
                    "from": patient_location,
                    "to": hospital_location,
                    "distance_km": transport_segment["distance_km"],
                    "time_minutes": transport_segment["time_minutes"],
                    "traffic_level": transport_segment["traffic_level"]
                }
            ]
            
            route["total_distance_km"] = pickup_segment["distance_km"] + transport_segment["distance_km"]
            route["total_time_minutes"] = pickup_segment["time_minutes"] + transport_segment["time_minutes"] + 10  # Loading time
            
            # Get traffic conditions
            route["traffic_conditions"] = self.traffic_model.get_current_traffic_conditions()
            
            # Generate alternative routes if available
            route["alternative_routes"] = self._generate_alternative_routes(
                ambulance_location, patient_location, hospital_location, priority
            )
            
        except Exception as e:
            logger.error(f"Route generation failed: {e}")
            route["error"] = str(e)
            
        return route
    
    def _generate_alternative_routes(self, ambulance_location: Tuple[float, float],
                                   patient_location: Tuple[float, float],
                                   hospital_location: Tuple[float, float],
                                   priority: int) -> List[Dict[str, Any]]:
        """Generate alternative route options"""
        alternatives = []
        
        # Alternative 1: Avoid high traffic areas
        try:
            alt_route = self.traffic_model.get_alternative_route(
                ambulance_location, patient_location, hospital_location, "avoid_traffic"
            )
            alternatives.append({
                "route_type": "avoid_traffic",
                "total_time_minutes": alt_route["time_minutes"],
                "description": "Route avoiding high traffic areas"
            })
        except:
            pass
        
        # Alternative 2: Shortest distance
        try:
            alt_route = self.traffic_model.get_alternative_route(
                ambulance_location, patient_location, hospital_location, "shortest_distance"
            )
            alternatives.append({
                "route_type": "shortest_distance", 
                "total_time_minutes": alt_route["time_minutes"],
                "description": "Shortest distance route"
            })
        except:
            pass
        
        return alternatives
    
    def _get_optimization_factors(self, evaluation: Dict[str, Any]) -> List[str]:
        """Get list of optimization factors for reporting"""
        factors = []
        
        for factor_name, factor_data in evaluation.get("factors", {}).items():
            score = factor_data.get("score", 0)
            if score >= 0.8:
                factors.append(f"Excellent {factor_name.replace('_', ' ')}")
            elif score >= 0.6:
                factors.append(f"Good {factor_name.replace('_', ' ')}")
            else:
                factors.append(f"Acceptable {factor_name.replace('_', ' ')}")
        
        return factors
    
    def get_optimization_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent optimization history"""
        return self.route_history[-limit:] if self.route_history else []
    
    def get_optimization_statistics(self) -> Dict[str, Any]:
        """Get optimization performance statistics"""
        if not self.route_history:
            return {"message": "No optimization history available"}
        
        recent_optimizations = self.route_history[-50:]  # Last 50 optimizations
        
        avg_time = sum(opt["total_time"] for opt in recent_optimizations) / len(recent_optimizations)
        priority_distribution = {}
        
        for opt in recent_optimizations:
            priority = opt["patient_priority"]
            priority_distribution[priority] = priority_distribution.get(priority, 0) + 1
        
        return {
            "total_optimizations": len(self.route_history),
            "average_total_time_minutes": round(avg_time, 1),
            "priority_distribution": priority_distribution,
            "optimization_success_rate": 95.0,  # Simulated success rate
            "average_improvement_percentage": 23.5  # Simulated improvement over basic routing
        }
    
    def invalidate_cache(self, older_than_minutes: int = 60):
        """Invalidate old optimization cache entries"""
        cutoff_time = datetime.now() - timedelta(minutes=older_than_minutes)
        
        to_remove = []
        for opt_id, opt_data in self.optimization_cache.items():
            opt_time = datetime.fromisoformat(opt_data["timestamp"])
            if opt_time < cutoff_time:
                to_remove.append(opt_id)
        
        for opt_id in to_remove:
            del self.optimization_cache[opt_id]
        
        if to_remove:
            logger.info(f"Invalidated {len(to_remove)} old optimization cache entries")
    
    def toi_uu(self, input_list):
        return input_list
