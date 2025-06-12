// Data visualization for patient flow
document.addEventListener('DOMContentLoaded', function() {
    // Check if the flow-graph element exists
    const flowGraphContainer = document.getElementById('flow-graph');
    if (!flowGraphContainer) return;

    // Get the current flow data
    fetch('/api/flows/current')
        .then(response => response.json())
        .then(data => {
            if (data && data.data && data.data.nodes) {
                renderFlowGraph(data.data);
            } else {
                flowGraphContainer.innerHTML = '<div class="alert alert-info">No flow data available. Run a demo to generate data.</div>';
            }
        })
        .catch(error => {
            console.error('Error fetching flow data:', error);
            flowGraphContainer.innerHTML = '<div class="alert alert-danger">Error loading flow data. Please try again later.</div>';
        });

    // Render flow graph using D3.js
    function renderFlowGraph(flowData) {
        const nodes = [];
        const links = [];

        // Convert nodes to array format for D3
        for (const nodeId in flowData.nodes) {
            nodes.push({
                id: nodeId,
                data: flowData.nodes[nodeId]
            });
        }

        // Add links from edges or sequence
        if (flowData.edges && flowData.edges.length > 0) {
            flowData.edges.forEach(edge => {
                links.push({
                    source: edge.source,
                    target: edge.target,
                    data: edge.data
                });
            });
        } else if (flowData.sequence && flowData.sequence.length > 1) {
            for (let i = 0; i < flowData.sequence.length - 1; i++) {
                links.push({
                    source: flowData.sequence[i],
                    target: flowData.sequence[i + 1]
                });
            }
        }

        if (nodes.length === 0) {
            flowGraphContainer.innerHTML = '<div class="alert alert-warning">No nodes found in flow data.</div>';
            return;
        }

        // Color mapping for different agent types
        const colorMap = {
            'TriageAgent': '#dc3545',     // Red
            'HospitalAgent': '#198754',   // Green
            'DispatchAgent': '#0dcaf0',   // Cyan
            'OptimizerAgent': '#6610f2',  // Purple
            'QAChatbotAgent': '#fd7e14'   // Orange
        };

        // Setup SVG
        const width = flowGraphContainer.clientWidth;
        const height = 400;
        
        // Clear previous content
        flowGraphContainer.innerHTML = '';
        
        const svg = d3.select('#flow-graph')
            .append('svg')
            .attr('width', width)
            .attr('height', height);

        // Add arrowhead marker definition
        svg.append('defs').append('marker')
            .attr('id', 'arrowhead')
            .attr('viewBox', '0 -5 10 10')
            .attr('refX', 25)
            .attr('refY', 0)
            .attr('orient', 'auto')
            .attr('markerWidth', 6)
            .attr('markerHeight', 6)
            .append('path')
            .attr('d', 'M0,-5L10,0L0,5')
            .attr('fill', '#999');

        // Create force simulation
        const simulation = d3.forceSimulation(nodes)
            .force('link', d3.forceLink(links).id(d => d.id).distance(150))
            .force('charge', d3.forceManyBody().strength(-500))
            .force('center', d3.forceCenter(width / 2, height / 2));

        // Create links
        const link = svg.append('g')
            .selectAll('line')
            .data(links)
            .join('line')
            .attr('stroke', '#999')
            .attr('stroke-opacity', 0.8)
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

        // Add circles to nodes
        node.append('circle')
            .attr('r', 25)
            .attr('fill', d => colorMap[d.id] || '#0d6efd')
            .attr('stroke', '#fff')
            .attr('stroke-width', 2);

        // Add labels to nodes
        node.append('text')
            .attr('text-anchor', 'middle')
            .attr('dy', '.35em')
            .attr('fill', '#fff')
            .text(d => d.id.replace('Agent', ''));

        // Add tooltips
        node.append('title')
            .text(d => {
                let tooltip = `${d.id}\n`;
                const input = d.data.input;
                const output = d.data.output;
                
                if (input) {
                    tooltip += '\nInput:\n';
                    if (typeof input === 'object') {
                        for (const [key, value] of Object.entries(input)) {
                            if (typeof value !== 'object') {
                                tooltip += `${key}: ${value}\n`;
                            }
                        }
                    }
                }
                
                if (output) {
                    tooltip += '\nOutput:\n';
                    if (typeof output === 'object') {
                        for (const [key, value] of Object.entries(output)) {
                            if (typeof value !== 'object') {
                                tooltip += `${key}: ${value}\n`;
                            }
                        }
                    }
                }
                
                return tooltip;
            });

        // Update positions on simulation tick
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

        // Add interaction for clicking on nodes
        node.on('click', function(event, d) {
            showNodeDetails(d.id, d.data);
        });
    }

    // Function to show node details in a modal
    function showNodeDetails(nodeId, data) {
        const modal = new bootstrap.Modal(document.getElementById('nodeDetailModal'));
        const modalTitle = document.querySelector('#nodeDetailModal .modal-title');
        const modalBody = document.querySelector('#nodeDetailModal .modal-body');
        
        modalTitle.textContent = nodeId;
        
        let content = `
            <div class="row">
                <div class="col-md-6">
                    <div class="card mb-3">
                        <div class="card-header bg-primary text-white">
                            <h5 class="card-title">Input Data</h5>
                        </div>
                        <div class="card-body">
                            <pre class="language-json">${JSON.stringify(data.input, null, 2)}</pre>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card mb-3">
                        <div class="card-header bg-success text-white">
                            <h5 class="card-title">Output Data</h5>
                        </div>
                        <div class="card-body">
                            <pre class="language-json">${JSON.stringify(data.output, null, 2)}</pre>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        modalBody.innerHTML = content;
        modal.show();
    }

    // Add event handler for Run Demo button
    document.getElementById('run-demo').addEventListener('click', function() {
        this.disabled = true;
        this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Running...';
        
        fetch('/api/run-demo', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showToast('Demo started successfully', 'success');
                setTimeout(() => {
                    window.location.reload();
                }, 5000); // Reload after 5 seconds
            } else {
                showToast('Error: ' + (data.error || 'Unknown error'), 'danger');
                this.disabled = false;
                this.textContent = 'Run Demo';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Error running demo', 'danger');
            this.disabled = false;
            this.textContent = 'Run Demo';
        });
    });

    // Function to show toast messages
    function showToast(message, type = 'info') {
        const toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        toastContainer.innerHTML = `
            <div class="toast align-items-center text-white bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body">
                        ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>
        `;
        
        document.body.appendChild(toastContainer);
        const toast = new bootstrap.Toast(toastContainer.querySelector('.toast'));
        toast.show();
        
        // Remove toast from DOM after it's hidden
        toastContainer.addEventListener('hidden.bs.toast', function() {
            document.body.removeChild(toastContainer);
        });
    }
});
