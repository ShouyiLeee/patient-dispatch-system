"""
FlowAgent - Simple optimization for patient routing
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import random

logger = logging.getLogger(__name__)

class FlowAgent:
    """
    Simple flow agent for patient routing optimization
    """
    
    def __init__(self):
        self.optimization_cache = {}
        self.route_history = []
        
    def optimize(self, hospitals_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Simple optimization - returns best hospital from list
        
        Args:
            hospitals_list: List of hospitals
            
        Returns:
            Dictionary with optimization result
        """
        if not hospitals_list:
            return {
                "type": "no_hospitals",
                "reason": "Không có bệnh viện phù hợp",
                "best_hospital": None
            }
        
        # Sort by distance and availability
        sorted_hospitals = sorted(hospitals_list, 
                                key=lambda h: (h.get('distance', 999), not h.get('available', True)))
        
        best_hospital = sorted_hospitals[0]
        
        return {
            "type": "optimization_complete",
            "reason": f"Chọn bệnh viện gần nhất và có sẵn",
            "best_hospital": best_hospital,
            "total_hospitals_evaluated": len(hospitals_list)
        }
    
    def toi_uu(self, data):
        """
        Vietnamese wrapper for optimize function (for compatibility)
        """
        return self.optimize(data)
