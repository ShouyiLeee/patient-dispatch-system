// main.js - Patient Flow Coordination System front-end logic

// Global variables
let currentFlow = null;
let flowHistory = [];
let flowGraph = null;

// Initialize page when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Fetch current flow data
    fetchCurrentFlow();
    
    // Fetch history
    fetchFlowHistory();
    
    // Set up event listeners
    document.getElementById('run-demo').addEventListener('click', runNewDemo);
    
    // Add node detail modal to body if it doesn't exist
    if (!document.getElementById('nodeDetailModal')) {
        const modalHtml = `
        <div class="modal fade" id="nodeDetailModal" tabindex="-1" aria-labelledby="nodeDetailModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-xl">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="nodeDetailModalLabel">Node Details</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <!-- Content will be dynamically inserted -->
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>`;
        
        document.body.insertAdjacentHTML('beforeend', modalHtml);
    }
});

// Fetch the current flow data
function fetchCurrentFlow() {
    fetch('/api/flows/current')
        .then(response => response.json())
        .then(data => {
            if (data && data.data) {
                currentFlow = data;
                displayCurrentFlow(data.data);
                renderFlowGraph(data.data);
            } else {
                displayEmptyState();
            }
        })
        .catch(error => {
            console.error('Error fetching current flow:', error);
            displayEmptyState();
        });
}

// Fetch flow history
function fetchFlowHistory() {
    fetch('/api/flows/history')
        .then(response => response.json())
        .then(data => {
            flowHistory = data;
            displayFlowHistory(data);
        })
        .catch(error => {
            console.error('Error fetching flow history:', error);
        });
}

// Run a new demo flow
function runNewDemo() {
    // Show loading indicators
    document.getElementById('flow-graph').innerHTML = `
        <div class="text-center p-5">
            <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p>Đang chạy demo mới...</p>
        </div>
    `;
    
    // Make API call to run demo
    fetch('/api/run-demo', {
        method: 'POST'
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Refresh data after a short delay to allow backend processing
                setTimeout(() => {
                    fetchCurrentFlow();
                    fetchFlowHistory();
                }, 1000);
            } else {
                alert('Có lỗi khi chạy demo: ' + (data.error || 'Lỗi không xác định'));
            }
        })
        .catch(error => {
            console.error('Error running demo:', error);
            alert('Có lỗi khi chạy demo. Xem console để biết chi tiết.');
        });
}

// Display current flow data
function displayCurrentFlow(flowData) {
    if (!flowData) return;
    
    // Display patient info
    let patientInfo = '';
    const firstNodeId = flowData.sequence[0];
    const firstNode = flowData.nodes[firstNodeId];
    
    if (firstNode && firstNode.input) {
        const patientData = firstNode.input;
        patientInfo = `
            <h6 class="mb-3">ID: ${patientData.patient_id || 'N/A'}</h6>
            <p><strong>Mô tả:</strong> ${patientData.description || 'Không có thông tin'}</p>
            <p><strong>Vị trí:</strong> ${formatLocation(patientData.location)}</p>
            <p><strong>Dấu hiệu sinh tồn:</strong> ${patientData.vitals || 'Không có thông tin'}</p>
            <p><strong>Thời gian bắt đầu:</strong> ${patientData.onset_time || 'Không xác định'}</p>
        `;
    }
    document.getElementById('patient-info').innerHTML = patientInfo || '<p>Không có thông tin bệnh nhân</p>';
    
    // Display triage info
    let triageInfo = '';
    const triageNode = flowData.nodes['TriageAgent'];
    if (triageNode && triageNode.output) {
        const triageData = triageNode.output;
        
        // Create symptom tags
        let symptomTags = '';
        if (triageData.symptoms && triageData.symptoms.length > 0) {
            triageData.symptoms.forEach(symptom => {
                symptomTags += `<span class="symptom-tag">${symptom.name} (${symptom.severity})</span>`;
            });
        }
        
        // Priority display with color coding
        const priorityClass = `priority-${triageData.priority || '3'}`;
        
        triageInfo = `
            <div class="mb-3">
                <span class="info-label">Mức độ ưu tiên:</span>
                <span class="triage-priority ${priorityClass}">${triageData.priority || '3'}/5</span>
            </div>
            <div class="mb-3">
                <span class="info-label">Chuyên khoa cần thiết:</span>
                <span>${triageData.specialty || 'Cấp cứu'}</span>
            </div>
            <div class="mb-3">
                <span class="info-label">Cần cấp cứu:</span>
                <span>${triageData.needs_emergency ? 'Có' : 'Không'}</span>
            </div>
            <div class="mt-3">
                <p class="info-label">Triệu chứng:</p>
                <div>${symptomTags || 'Không có thông tin'}</div>
            </div>
        `;
    }
    document.getElementById('triage-info').innerHTML = triageInfo || '<p>Không có thông tin phân loại</p>';
    
    // Display hospital info
    let hospitalInfo = '';
    const optimizerNode = flowData.nodes['OptimizerAgent'];
    if (optimizerNode && optimizerNode.output && optimizerNode.output.optimized_hospital) {
        const hospital = optimizerNode.output.optimized_hospital;
        
        // Get more details from hospital node if available
        const hospitalNode = flowData.nodes['HospitalAgent'];
        let doctorInfo = '';
        if (hospitalNode && hospitalNode.output && hospitalNode.output.hospitals) {
            const matchedHospital = hospitalNode.output.hospitals.find(h => h.id === hospital.id);
            if (matchedHospital && matchedHospital.assigned_doctor) {
                const doctor = matchedHospital.assigned_doctor;
                doctorInfo = `
                    <div class="mt-3">
                        <p class="info-label">Bác sĩ được chỉ định:</p>
                        <p class="doctor-name">${doctor.name} (${doctor.id})</p>
                        <p>Chuyên khoa: ${matchedHospital.doctor_specialty || 'Không xác định'}</p>
                    </div>
                `;
            }
        }
        
        hospitalInfo = `
            <h6 class="mb-3">${hospital.name} (${hospital.id})</h6>
            <p><span class="info-label">Địa chỉ:</span> ${hospital.address || 'Không có thông tin'}</p>
            <p><span class="info-label">Khoảng cách:</span> ${hospital.estimated_distance_km || '?'} km</p>
            <p><span class="info-label">Thời gian chờ:</span> ${hospital.wait_time_minutes || '?'} phút</p>
            ${doctorInfo}
        `;
    }
    document.getElementById('hospital-info').innerHTML = hospitalInfo || '<p>Không có thông tin bệnh viện</p>';
    
    // Display ambulance info
    let ambulanceInfo = '';
    if (optimizerNode && optimizerNode.output && optimizerNode.output.optimized_ambulance) {
        const ambulance = optimizerNode.output.optimized_ambulance;
        
        // Get more details from dispatch node if available
        const dispatchNode = flowData.nodes['DispatchAgent'];
        let personnelInfo = '';
        if (dispatchNode && dispatchNode.output && dispatchNode.output.ambulances) {
            const matchedAmbulance = dispatchNode.output.ambulances.find(a => a.id === ambulance.id);
            if (matchedAmbulance && matchedAmbulance.personnel && matchedAmbulance.personnel.length > 0) {
                personnelInfo = '<div class="mt-3"><p class="info-label">Nhân viên:</p><ul>';
                matchedAmbulance.personnel.forEach(person => {
                    personnelInfo += `<li>${person.name} - ${person.role}</li>`;
                });
                personnelInfo += '</ul></div>';
            }
        }
        
        ambulanceInfo = `
            <h6 class="mb-3">${ambulance.name} (${ambulance.id})</h6>
            <p><span class="info-label">Trang thiết bị:</span> ${
                ambulance.equipment ? ambulance.equipment.join(', ') : 'Không có thông tin'
            }</p>
            <p><span class="info-label">Thời gian đến dự kiến:</span> <span class="eta">${ambulance.eta_minutes || '?'} phút</span></p>
            ${personnelInfo}
            <p class="mt-3"><span class="info-label">Thời gian đến bệnh viện dự kiến:</span> <strong>${optimizerNode.output.estimated_arrival_time || 'Không xác định'}</strong></p>
        `;
    }
    document.getElementById('ambulance-info').innerHTML = ambulanceInfo || '<p>Không có thông tin xe cứu thương</p>';
}

// Render flow graph using D3.js
function renderFlowGraph(flowData) {
    // Clear previous graph
    document.getElementById('flow-graph').innerHTML = '';
    
    // Create nodes and links from flow data
    const nodes = [];
    const links = [];
    
    // Add nodes
    for (const nodeId in flowData.nodes) {
        nodes.push({
            id: nodeId,
            name: nodeId.replace('Agent', '')
        });
    }
    
    // Add links from sequence or edges
    if (flowData.edges && flowData.edges.length > 0) {
        // Use explicit edges if available
        flowData.edges.forEach(edge => {
            links.push({
                source: edge.source,
                target: edge.target
            });
        });
    } else if (flowData.sequence && flowData.sequence.length > 1) {
        // Fall back to sequence
        for (let i = 0; i < flowData.sequence.length - 1; i++) {
            links.push({
                source: flowData.sequence[i],
                target: flowData.sequence[i + 1]
            });
        }
    }
    
    // Set up D3 visualization
    const width = document.getElementById('flow-graph').clientWidth;
    const height = 400;
    
    const svg = d3.select('#flow-graph')
        .append('svg')
        .attr('width', width)
        .attr('height', height);
    
    // Define colors for nodes
    const colors = {
        'Triage': '#dc3545',      // Red
        'Hospital': '#198754',    // Green
        'Dispatch': '#0dcaf0',    // Cyan
        'Optimizer': '#6f42c1',   // Purple
        'QA': '#fd7e14'           // Orange
    };
    
    // Set up force simulation
    const simulation = d3.forceSimulation(nodes)
        .force('link', d3.forceLink(links).id(d => d.id).distance(120))
        .force('charge', d3.forceManyBody().strength(-400))
        .force('center', d3.forceCenter(width / 2, height / 2));
    
    // Create arrow marker for directed edges
    svg.append('defs').append('marker')
        .attr('id', 'arrowhead')
        .attr('viewBox', '-0 -5 10 10')
        .attr('refX', 20)
        .attr('refY', 0)
        .attr('orient', 'auto')
        .attr('markerWidth', 6)
        .attr('markerHeight', 6)
        .attr('xoverflow', 'visible')
        .append('svg:path')
        .attr('d', 'M 0,-5 L 10,0 L 0,5')
        .attr('fill', '#999')
        .attr('stroke', 'none');
    
    // Draw links
    const link = svg.append('g')
        .selectAll('line')
        .data(links)
        .join('line')
        .attr('class', 'link')
        .attr('stroke-width', 2)
        .attr('marker-end', 'url(#arrowhead)');
    
    // Create node groups
    const node = svg.append('g')
        .selectAll('.node')
        .data(nodes)
        .join('g')
        .attr('class', 'node')
        .call(d3.drag()
            .on('start', dragstarted)
            .on('drag', dragged)
            .on('end', dragended));
    
    // Add circles for nodes
    node.append('circle')
        .attr('r', 30)
        .attr('fill', d => {
            const type = d.name;
            return colors[type] || '#0d6efd';
        })
        .attr('stroke', '#fff')
        .attr('stroke-width', 2);
    
    // Add labels to nodes
    node.append('text')
        .attr('class', 'node-label')
        .attr('dy', '.35em')
        .attr('fill', 'white')
        .attr('text-anchor', 'middle')
        .text(d => d.name);
    
    // Add tooltip
    node.on('mouseover', function(event, d) {
        const nodeData = flowData.nodes[d.id];
        const tooltipContent = formatNodeTooltip(d.id, nodeData);
        
        d3.select('body').append('div')
            .attr('class', 'tooltip-custom')
            .html(tooltipContent)
            .style('left', (event.pageX + 15) + 'px')
            .style('top', (event.pageY - 28) + 'px');
    })
    .on('mouseout', function() {
        d3.select('.tooltip-custom').remove();
    });
    
    // Update positions on each tick
    simulation.on('tick', () => {
        link
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);
        
        node
            .attr('transform', d => `translate(${d.x},${d.y})`);
    });
    
    // Drag functions
    function dragstarted(event) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        event.subject.fx = event.subject.x;
        event.subject.fy = event.subject.y;
    }
    
    function dragged(event) {
        event.subject.fx = event.x;
        event.subject.fy = event.y;
    }
    
    function dragended(event) {
        if (!event.active) simulation.alphaTarget(0);
        event.subject.fx = null;
        event.subject.fy = null;
    }
}

// Display flow history
function displayFlowHistory(history) {
    const tableBody = document.getElementById('history-body');
    if (!tableBody) return;
    
    tableBody.innerHTML = '';
    
    if (!history || history.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="6" class="text-center">Không có dữ liệu lịch sử</td></tr>';
        return;
    }
    
    history.forEach(item => {
        const row = document.createElement('tr');
        
        // Format ID for better display
        const shortId = item.id.split('_').pop().substring(0, 8); 
        
        row.innerHTML = `
            <td>${shortId}</td>
            <td>${formatTimestamp(item.timestamp)}</td>
            <td>ID: ${item.patient_id || 'N/A'}</td>
            <td>${item.hospital || 'N/A'}</td>
            <td>${item.ambulance || 'N/A'}</td>
            <td>
                <button class="btn btn-sm btn-primary view-flow" data-id="${item.id}">Xem</button>
            </td>
        `;
        
        tableBody.appendChild(row);
    });
    
    // Add event listeners to view buttons
    document.querySelectorAll('.view-flow').forEach(button => {
        button.addEventListener('click', function() {
            const flowId = this.getAttribute('data-id');
            viewFlowDetail(flowId);
        });
    });
}

// View flow detail
function viewFlowDetail(flowId) {
    fetch(`/api/flows/${flowId}`)
        .then(response => response.json())
        .then(data => {
            if (data && data.data) {
                // Populate modal with flow details
                document.getElementById('flow-detail-content').innerHTML = formatFlowDetail(data.data);
                
                // Show modal
                const modal = new bootstrap.Modal(document.getElementById('flowDetailModal'));
                modal.show();
            }
        })
        .catch(error => {
            console.error('Error fetching flow detail:', error);
            alert('Có lỗi khi tải chi tiết luồng dữ liệu.');
        });
}

// Format flow detail for modal
function formatFlowDetail(flowData) {
    let content = `
        <div class="flow-detail">
            <h5>Thông tin chi tiết luồng dữ liệu</h5>
            <p><strong>Thời gian:</strong> ${formatTimestamp(flowData.timestamp)}</p>
            
            <div class="mt-4">
                <h6>Tuần tự xử lý:</h6>
                <ol>
    `;
    
    // Add sequence steps
    if (flowData.sequence && flowData.sequence.length > 0) {
        flowData.sequence.forEach(step => {
            content += `<li>${step}</li>`;
        });
    } else {
        content += '<li>Không có dữ liệu tuần tự</li>';
    }
    
    content += `
                </ol>
            </div>
            
            <div class="mt-4">
                <h6>Chi tiết các node:</h6>
                <div class="accordion" id="nodeAccordion">
    `;
    
    // Add node details as accordion items
    let nodeIndex = 0;
    for (const nodeId in flowData.nodes) {
        const node = flowData.nodes[nodeId];
        const nodeIdSafe = `node_${nodeIndex}`;
        
        content += `
            <div class="accordion-item">
                <h2 class="accordion-header" id="heading_${nodeIdSafe}">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" 
                            data-bs-target="#collapse_${nodeIdSafe}" aria-expanded="false" 
                            aria-controls="collapse_${nodeIdSafe}">
                        ${nodeId}
                    </button>
                </h2>
                <div id="collapse_${nodeIdSafe}" class="accordion-collapse collapse" 
                     aria-labelledby="heading_${nodeIdSafe}" data-bs-parent="#nodeAccordion">
                    <div class="accordion-body">
                        <div class="row">
                            <div class="col-md-6">
                                <h6>Dữ liệu đầu vào:</h6>
                                <pre class="bg-light p-3 rounded">${formatJSONForDisplay(node.input)}</pre>
                            </div>
                            <div class="col-md-6">
                                <h6>Dữ liệu đầu ra:</h6>
                                <pre class="bg-light p-3 rounded">${formatJSONForDisplay(node.output)}</pre>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        nodeIndex++;
    }
    
    content += `
                </div>
            </div>
        </div>
    `;
    
    return content;
}

// Helper functions
function formatLocation(location) {
    if (!location || !location.latitude || !location.longitude) return 'Không có thông tin';
    return `${location.latitude.toFixed(4)}, ${location.longitude.toFixed(4)}`;
}

function formatTimestamp(timestamp) {
    if (!timestamp) return 'N/A';
    
    // Convert to readable format
    const date = new Date(timestamp);
    if (isNaN(date.getTime())) {
        // Parse common format: '2025-06-12 01:48:12'
        const parts = timestamp.split(' ');
        if (parts.length === 2) {
            const dateParts = parts[0].split('-');
            const timeParts = parts[1].split(':');
            if (dateParts.length === 3 && timeParts.length === 3) {
                return `${dateParts[2]}/${dateParts[1]}/${dateParts[0]} ${parts[1]}`;
            }
        }
        return timestamp;
    }
    
    return date.toLocaleString('vi-VN');
}

function formatJSONForDisplay(obj) {
    if (!obj) return 'Không có dữ liệu';
    try {
        return JSON.stringify(obj, null, 2);
    } catch (e) {
        return String(obj);
    }
}

function formatNodeTooltip(nodeId, nodeData) {
    if (!nodeData) return `<strong>${nodeId}</strong><br>Không có dữ liệu`;
    
    let tooltipContent = `<strong>${nodeId}</strong>`;
    
    if (nodeData.input) {
        tooltipContent += '<br><br><em>Input:</em><br>';
        
        if (typeof nodeData.input === 'object') {
            for (const key in nodeData.input) {
                const value = nodeData.input[key];
                if (typeof value !== 'object') {
                    tooltipContent += `${key}: ${value}<br>`;
                }
            }
        } else {
            tooltipContent += String(nodeData.input).substring(0, 50);
        }
    }
    
    if (nodeData.output) {
        tooltipContent += '<br><em>Output:</em><br>';
        
        if (typeof nodeData.output === 'object') {
            for (const key in nodeData.output) {
                const value = nodeData.output[key];
                if (typeof value !== 'object') {
                    tooltipContent += `${key}: ${value}<br>`;
                }
            }
        } else {
            tooltipContent += String(nodeData.output).substring(0, 50);
        }
    }
    
    return tooltipContent;
}

function displayEmptyState() {
    document.getElementById('patient-info').innerHTML = '<p>Không có dữ liệu bệnh nhân</p>';
    document.getElementById('triage-info').innerHTML = '<p>Không có dữ liệu phân loại</p>';
    document.getElementById('hospital-info').innerHTML = '<p>Không có dữ liệu bệnh viện</p>';
    document.getElementById('ambulance-info').innerHTML = '<p>Không có dữ liệu xe cứu thương</p>';
    
    document.getElementById('flow-graph').innerHTML = `
        <div class="text-center p-5">
            <p>Chưa có dữ liệu luồng. Nhấn nút "Chạy Demo Mới" để bắt đầu.</p>
        </div>
    `;
}
