import json
import matplotlib.pyplot as plt
import networkx as nx
from datetime import datetime
import os

class FlowTracker:
    """
    Lớp theo dõi và visualize flow của dữ liệu thông qua các agent trong hệ thống.
    Flow tracker lưu trữ và hiển thị dữ liệu đi qua mỗi node, giúp debug và theo dõi.
    """
    def __init__(self, flow_name="patient_flow", save_dir="flow_logs"):
        self.flow_name = flow_name
        self.save_dir = save_dir
        self.flow_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nodes": {},
            "edges": [],
            "sequence": []
        }
        
        # Tạo thư mục lưu flow logs nếu chưa tồn tại
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
    def track_node(self, node_id, input_data, output_data):
        """
        Theo dõi dữ liệu đi qua một node (agent)
        """
        self.flow_data["nodes"][node_id] = {
            "input": input_data,
            "output": output_data,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.flow_data["sequence"].append(node_id)
        
        # Lưu log sau mỗi lần cập nhật
        self._save_flow_log()
        
    def track_edge(self, source_id, target_id, data=None):
        """
        Theo dõi dữ liệu trên một edge (liên kết)
        """
        edge = {
            "source": source_id,
            "target": target_id,
            "data": data,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.flow_data["edges"].append(edge)
        
        # Lưu log sau mỗi lần cập nhật
        self._save_flow_log()
    
    def _save_flow_log(self):
        """Lưu flow log vào file JSON"""
        filename = f"{self.save_dir}/{self.flow_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.flow_data, f, ensure_ascii=False, indent=2)
        
    # def visualize(self, title=None):
    #     """
    #     Hiển thị flow graph với dữ liệu ở mỗi node
    #     """
    #     G = nx.DiGraph()
        
    #     # Thêm các nodes từ dữ liệu đã theo dõi
    #     for node_id, node_data in self.flow_data["nodes"].items():
    #         # Tóm tắt input/output để hiển thị trong node label
    #         input_summary = self._summarize_data(node_data["input"])
    #         output_summary = self._summarize_data(node_data["output"])
            
    #         node_label = f"{node_id}\nInput: {input_summary}\nOutput: {output_summary}"
    #         G.add_node(node_id, label=node_label, data=node_data)
        
    #     # Thêm các edges
    #     for edge in self.flow_data["edges"]:
    #         G.add_edge(edge["source"], edge["target"])
        
    #     # Nếu không có edges được theo dõi, tạo edges theo sequence
    #     if not G.edges():
    #         for i in range(len(self.flow_data["sequence"]) - 1):
    #             source = self.flow_data["sequence"][i]
    #             target = self.flow_data["sequence"][i+1]
    #             G.add_edge(source, target)
        
    #     # Tạo layout cho đồ thị
    #     pos = nx.spring_layout(G) if len(G.nodes()) > 1 else {list(G.nodes())[0]: (0, 0)}
        
    #     # Vẽ đồ thị
    #     plt.figure(figsize=(12, 8))
        
    #     # Vẽ nodes
    #     for node, (x, y) in pos.items():
    #         nx.draw_networkx_nodes(G, {node: (x, y)}, nodelist=[node], 
    #                                node_color='lightblue', node_size=3000, alpha=0.8)
            
    #         # Tạo label text với thông tin input/output
    #         node_label = node
    #         if node in G.nodes:
    #             node_data = G.nodes[node].get("data", {})
    #             input_data = node_data.get("input", {})
    #             output_data = node_data.get("output", {})
                
    #             # Hiển thị tóm tắt thông tin
    #             plt.text(x, y-0.12, f"IN: {self._summarize_data(input_data)}", 
    #                      horizontalalignment='center', fontsize=8)
    #             plt.text(x, y, node, horizontalalignment='center', 
    #                      verticalalignment='center', fontsize=10, fontweight='bold')
    #             plt.text(x, y+0.12, f"OUT: {self._summarize_data(output_data)}", 
    #                      horizontalalignment='center', fontsize=8)
        
    #     # Vẽ edges
    #     nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.7, arrowsize=20)
        
    #     # Thêm labels
    #     # nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")
        
    #     # Thêm tiêu đề
    #     plt.title(title or f"Flow Visualization: {self.flow_name}")
    #     plt.axis('off')
        
    #     # Lưu ảnh
    #     filename = f"{self.save_dir}/{self.flow_name}_visualization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    #     plt.savefig(filename, dpi=200, bbox_inches='tight')
    #     plt.show()
        
    #     return filename
    
    def _summarize_data(self, data, max_len=50):
        """Tóm tắt dữ liệu để hiển thị trong node"""
        if isinstance(data, dict):
            if len(data) == 0:
                return "{}"
            keys = list(data.keys())
            if len(keys) > 2:
                return f"{{{keys[0]}, {keys[1]}, ...}}"
            return str(data)
        elif isinstance(data, list):
            if len(data) == 0:
                return "[]"
            if len(data) > 2:
                return f"[{data[0]}, ...]"
            return str(data)
        elif isinstance(data, str):
            if len(data) > max_len:
                return data[:max_len] + "..."
            return data
        else:
            return str(data)

# Ví dụ sử dụng FlowTracker
if __name__ == "__main__":
    # Demo với dữ liệu mẫu
    tracker = FlowTracker(flow_name="patient_flow_demo")
    
    # Mô phỏng luồng bệnh nhân qua các agent
    input_data = {
        "patient_id": "P12345",
        "description": "Nam, 55 tuổi, bất tỉnh trong công viên, da tái, mồ hôi lạnh, không phản ứng.",
        "location": {"latitude": 10.754, "longitude": 106.6631},
        "vitals": "Huyết áp: Không đo được, Nhịp tim: Không xác định",
        "onset_time": "10 phút",
        "medical_history": "Tăng huyết áp, đái tháo đường"
    }
    
    # Theo dõi TriageAgent
    triage_output = {
        "symptoms": [
            {"name": "Bất tỉnh", "severity": "Cao"},
            {"name": "Da tái", "severity": "Cao"},
            {"name": "Mồ hôi lạnh", "severity": "Trung bình"}
        ],
        "priority": 5,
        "specialty": "Tim mạch",
        "needs_emergency": True
    }
    tracker.track_node("TriageAgent", input_data, triage_output)
    
    # Theo dõi HospitalAgent
    hospital_input = {**triage_output, "patient_id": "P12345"}
    hospital_output = {
        "patient_id": "P12345",
        "hospitals": [
            {"id": "H001", "name": "Bệnh viện Chợ Rẫy", "distance_km": 2.3, "specialty_match": True},
            {"id": "H003", "name": "Bệnh viện Nhân Dân Gia Định", "distance_km": 5.1, "specialty_match": True}
        ],
        "is_emergency": True
    }
    tracker.track_node("HospitalAgent", hospital_input, hospital_output)
    tracker.track_edge("TriageAgent", "HospitalAgent", triage_output)
    
    # Theo dõi DispatchAgent
    dispatch_input = {**triage_output, "patient_id": "P12345"}
    dispatch_output = {
        "patient_id": "P12345",
        "ambulances": [
            {"id": "A001", "name": "Xe cứu thương 1", "eta_minutes": 7},
            {"id": "A002", "name": "Xe cứu thương 2", "eta_minutes": 12}
        ],
        "is_emergency": True
    }
    tracker.track_node("DispatchAgent", dispatch_input, dispatch_output)
    tracker.track_edge("TriageAgent", "DispatchAgent", triage_output)
    
    # Theo dõi OptimizerAgent
    optimizer_input = {
        "hospital_data": hospital_output,
        "dispatch_data": dispatch_output
    }
    optimizer_output = {
        "patient_id": "P12345",
        "optimized_hospital": {"id": "H001", "name": "Bệnh viện Chợ Rẫy"},
        "optimized_ambulance": {"id": "A001", "name": "Xe cứu thương 1"},
        "eta_minutes": 7,
        "estimated_arrival_time": "14:25"
    }
    tracker.track_node("OptimizerAgent", optimizer_input, optimizer_output)
    tracker.track_edge("HospitalAgent", "OptimizerAgent", hospital_output)
    tracker.track_edge("DispatchAgent", "OptimizerAgent", dispatch_output)
    
    # Visualize flow
    # tracker.visualize("Patient Flow Coordination Demo")
