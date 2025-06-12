"""
Generate HTML reports for flow visualization
"""
import json
import os
from datetime import datetime

def generate_html_report(flow_data, output_dir="static", filename=None):
    """
    Generate an HTML report for flow visualization
    
    Args:
        flow_data: Dictionary containing flow data
        output_dir: Directory to save HTML file
        filename: Optional filename for HTML report
        
    Returns:
        Path to generated HTML file
    """
    os.makedirs(output_dir, exist_ok=True)
    
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"flow_report_{timestamp}.html"
        
    output_path = os.path.join(output_dir, filename)
    
    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Patient Flow Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background-color: #0d6efd; color: white; padding: 15px; text-align: center; }}
        .node {{ border: 1px solid #ccc; margin: 20px 0; padding: 15px; border-radius: 5px; }}
        .node-title {{ background-color: #f0f0f0; padding: 5px; margin: -15px -15px 15px; border-radius: 5px 5px 0 0; }}
        .edge {{ margin: 10px 0; padding: 10px; background-color: #f9f9f9; border-left: 4px solid #0d6efd; }}
        .data-section {{ display: flex; }}
        .data-column {{ flex: 1; padding: 10px; }}
        pre {{ background-color: #f5f5f5; padding: 10px; overflow-x: auto; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Patient Flow Coordination Report</h1>
            <p>Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
        
        <h2>Flow Sequence</h2>
        <ol>
"""

    # Add sequence
    for node_id in flow_data.get("sequence", []):
        html_content += f"            <li>{node_id}</li>\n"
    
    html_content += """        </ol>
        
        <h2>Nodes</h2>
"""

    # Add nodes
    for node_id, node_data in flow_data.get("nodes", {}).items():
        input_data = json.dumps(node_data.get("input", {}), indent=2)
        output_data = json.dumps(node_data.get("output", {}), indent=2)
        
        html_content += f"""
        <div class="node">
            <div class="node-title">
                <h3>{node_id}</h3>
                <p>Timestamp: {node_data.get("timestamp", "Unknown")}</p>
            </div>
            
            <div class="data-section">
                <div class="data-column">
                    <h4>Input Data</h4>
                    <pre>{input_data}</pre>
                </div>
                <div class="data-column">
                    <h4>Output Data</h4>
                    <pre>{output_data}</pre>
                </div>
            </div>
        </div>
"""

    html_content += """
        <h2>Edges</h2>
"""

    # Add edges
    for edge in flow_data.get("edges", []):
        edge_data = json.dumps(edge.get("data", {}), indent=2)
        
        html_content += f"""
        <div class="edge">
            <h4>{edge.get("source", "Unknown")} → {edge.get("target", "Unknown")}</h4>
            <p>Timestamp: {edge.get("timestamp", "Unknown")}</p>
            <h5>Data:</h5>
            <pre>{edge_data}</pre>
        </div>
"""

    html_content += """
    </div>
</body>
</html>"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    return output_path
