const processPatientCare = document.createElement('script');
processPatientCare.innerHTML = `
function updatePatientCareStep(data) {
    // Update UI
    document.getElementById('patient-care-step').classList.add('timeline-item-active');
    document.getElementById('patient-care-time').textContent = new Date().toLocaleTimeString();
    
    // Remove spinner and show result
    let patientCareBody = document.getElementById('patient-care-step').querySelector('.timeline-body');
    patientCareBody.innerHTML = "";
    
    let resultDiv = document.getElementById('patient-care-result');
    resultDiv.classList.remove('d-none');
    
    // Format patient care results
    let routeText = "";
    let routeClass = "";
    
    switch(data.route_to) {
        case 'chatbot':
            routeText = "Tư vấn trực tuyến";
            routeClass = "info";
            break;
        case 'hospital':
            routeText = "Bệnh viện";
            routeClass = "warning";
            break;
        case 'emergency':
            routeText = "Cấp cứu";
            routeClass = "danger";
            break;
        default:
            routeText = "Không xác định";
            routeClass = "secondary";
    }
    
    let resultHTML = \`
        <div class="alert alert-\${routeClass} mb-2">
            <strong>Quyết định:</strong> \${data.message || 'Đang phân luồng bệnh nhân'}
        </div>
        <strong>Điều hướng đến:</strong> <span class="badge bg-\${routeClass}">\${routeText}</span><br>
    \`;
    
    resultDiv.innerHTML = resultHTML;
    patientCareBody.appendChild(resultDiv);
}

// Hook into the socket event
socket.on('patient_care_update', function(data) {
    updatePatientCareStep(data);
    // Update the regular progress bar
    currentStep = 2;
    const percent = Math.min(Math.round((currentStep / totalSteps) * 100), 100);
    document.getElementById('progress-bar').style.width = percent + '%';
    document.getElementById('progress-bar').textContent = percent + '%';
    
    // Update the next step badge
    if (data.route_to === 'chatbot') {
        document.getElementById('processing-message').textContent = 'Chuẩn bị chuyển đến tư vấn trực tuyến...';
    } else if (data.route_to === 'hospital') {
        document.getElementById('processing-message').textContent = 'Đang tìm bệnh viện phù hợp...';
    } else if (data.route_to === 'emergency') {
        document.getElementById('processing-message').textContent = 'Đang tìm xe cứu thương và bệnh viện...';
    }
});
`;
document.body.appendChild(processPatientCare);
