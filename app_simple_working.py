"""
Simple Working Web Application for Patient Dispatch System
Uses the tested clean workflow with mock agents
"""

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import threading
import json
import logging
from datetime import datetime
import uuid

# Import our working clean workflow
from test_clean_workflow import SimplePatientDispatchWorkflow

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'patient_dispatch_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize workflow
workflow = SimplePatientDispatchWorkflow()

# Store active sessions
active_sessions = {}

@app.route('/')
def index():
    """Main page"""
    return render_template('simple_working_interface.html')

@app.route('/api/process_patient', methods=['POST'])
def process_patient():
    """API endpoint to process patient data"""
    try:
        # Get patient data from request
        patient_data = request.json
        session_id = str(uuid.uuid4())
        
        # Store session
        active_sessions[session_id] = {
            'status': 'processing',
            'start_time': datetime.now(),
            'patient_data': patient_data
        }
        
        # Start workflow in background thread
        thread = threading.Thread(
            target=run_workflow_with_progress,
            args=(session_id, patient_data)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'Bắt đầu xử lý bệnh nhân'
        })
        
    except Exception as e:
        logger.error(f"Error processing patient: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def run_workflow_with_progress(session_id, patient_data):
    """Run workflow with real-time progress updates"""
    try:
        # Initialize progress
        socketio.emit('workflow_start', {
            'session_id': session_id,
            'message': 'Bắt đầu quy trình điều phối bệnh nhân'
        })
        
        # Step 1: Information Extraction
        socketio.emit('workflow_progress', {
            'session_id': session_id,
            'step': 1,
            'step_name': 'Trích xuất thông tin bệnh nhân',
            'status': 'processing',
            'message': 'Đang phân tích mô tả và triệu chứng...'
        })
        
        # Simulate some processing time
        import time
        time.sleep(1)
        
        extraction_result = workflow.extract_patient_information(patient_data)
        
        socketio.emit('workflow_progress', {
            'session_id': session_id,
            'step': 1,
            'step_name': 'Trích xuất thông tin bệnh nhân',
            'status': 'completed',
            'result': extraction_result,
            'message': f"Đã trích xuất {len(extraction_result.get('extracted_symptoms', []))} triệu chứng"
        })
        
        # Step 2: Triage Assessment
        socketio.emit('workflow_progress', {
            'session_id': session_id,
            'step': 2,
            'step_name': 'Đánh giá phân loại bệnh nhân',
            'status': 'processing',
            'message': 'Đang đánh giá mức độ ưu tiên...'
        })
        
        time.sleep(1)
        triage_result = workflow.perform_triage_assessment(extraction_result)
        
        socketio.emit('workflow_progress', {
            'session_id': session_id,
            'step': 2,
            'step_name': 'Đánh giá phân loại bệnh nhân',
            'status': 'completed',
            'result': triage_result,
            'message': f"Mức độ ưu tiên: {triage_result.get('priority_score', 0)}/5 - {triage_result.get('urgency_level', 'N/A')}"
        })
        
        # Step 3: Routing Decision
        socketio.emit('workflow_progress', {
            'session_id': session_id,
            'step': 3,
            'step_name': 'Quyết định tuyến điều trị',
            'status': 'processing',
            'message': 'Đang xác định tuyến điều trị phù hợp...'
        })
        
        time.sleep(1)
        routing_result = workflow.make_routing_decision(triage_result)
        
        socketio.emit('workflow_progress', {
            'session_id': session_id,
            'step': 3,
            'step_name': 'Quyết định tuyến điều trị',
            'status': 'completed',
            'result': routing_result,
            'message': f"Tuyến điều trị: {routing_result.get('route_description', 'N/A')}"
        })
        
        # Step 4: Execute Routing
        socketio.emit('workflow_progress', {
            'session_id': session_id,
            'step': 4,
            'step_name': 'Thực hiện điều phối',
            'status': 'processing',
            'message': f"Đang thực hiện {routing_result.get('route_description', 'điều phối')}..."
        })
        
        time.sleep(1)
        execution_result = workflow.execute_routing(routing_result, patient_data)
        
        socketio.emit('workflow_progress', {
            'session_id': session_id,
            'step': 4,
            'step_name': 'Thực hiện điều phối',
            'status': 'completed',
            'result': execution_result,
            'message': execution_result.get('message', 'Hoàn thành điều phối')
        })
        
        # Step 5: Final Optimization
        socketio.emit('workflow_progress', {
            'session_id': session_id,
            'step': 5,
            'step_name': 'Tối ưu hóa cuối cùng',
            'status': 'processing',
            'message': 'Đang tối ưu hóa kết quả...'
        })
        
        time.sleep(1)
        final_result = workflow.optimize_assignment(execution_result)
        
        socketio.emit('workflow_progress', {
            'session_id': session_id,
            'step': 5,
            'step_name': 'Tối ưu hóa cuối cùng',
            'status': 'completed',
            'result': final_result,
            'message': 'Hoàn thành quy trình điều phối bệnh nhân'
        })
        
        # Send final completion
        socketio.emit('workflow_complete', {
            'session_id': session_id,
            'final_result': final_result,
            'completion_time': datetime.now().isoformat()
        })
        
        # Update session
        active_sessions[session_id]['status'] = 'completed'
        active_sessions[session_id]['final_result'] = final_result
        
    except Exception as e:
        logger.error(f"Workflow error for session {session_id}: {e}")
        socketio.emit('workflow_error', {
            'session_id': session_id,
            'error': str(e),
            'message': 'Có lỗi xảy ra trong quá trình xử lý'
        })
        
        active_sessions[session_id]['status'] = 'error'
        active_sessions[session_id]['error'] = str(e)

@app.route('/api/qa_chat', methods=['POST'])
def qa_chat():
    """QA chat endpoint"""
    try:
        data = request.json
        question = data.get('question', '')
        context = data.get('context', '')
        
        response = workflow.qa_chatbot.ask_question(question, context)
        
        return jsonify({
            'success': True,
            'response': response
        })
        
    except Exception as e:
        logger.error(f"QA chat error: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'response': {
                'answer': 'Xin lỗi, có lỗi xảy ra. Vui lòng thử lại sau.'
            }
        }), 500

@app.route('/api/test_cases')
def get_test_cases():
    """Get predefined test cases"""
    test_cases = [
        {
            'name': 'Bệnh nhân thông thường',
            'description': 'Bệnh nhân nam, 35 tuổi, sốt nhẹ 2 ngày, ho khan, không khó thở',
            'vital_signs': {
                'heart_rate': 88,
                'blood_pressure': '120/80',
                'spo2': 98,
                'temperature': 37.5
            },
            'location': {
                'latitude': 10.77,
                'longitude': 106.67
            }
        },
        {
            'name': 'Bệnh nhân khẩn cấp',
            'description': 'Bệnh nhân nam, 45 tuổi, đau bụng dữ dội từ sáng, nôn mửa nhiều',
            'vital_signs': {
                'heart_rate': 105,
                'blood_pressure': '140/90',
                'spo2': 95,
                'temperature': 38.2
            },
            'location': {
                'latitude': 10.76,
                'longitude': 106.66
            }
        },
        {
            'name': 'Bệnh nhân cấp cứu',
            'description': 'Bệnh nhân nữ, 60 tuổi, đau ngực dữ dội, khó thở, choáng váng',
            'vital_signs': {
                'heart_rate': 130,
                'blood_pressure': '180/110',
                'spo2': 88,
                'temperature': 36.8
            },
            'location': {
                'latitude': 10.78,
                'longitude': 106.68
            }
        }
    ]
    
    return jsonify({
        'success': True,
        'test_cases': test_cases
    })

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info(f"Client connected: {request.sid}")
    emit('connected', {'message': 'Kết nối thành công với server'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info(f"Client disconnected: {request.sid}")

if __name__ == '__main__':
    print("=" * 60)
    print("🏥 PATIENT DISPATCH SYSTEM")
    print("=" * 60)
    print("✅ Workflow tested and working")
    print("✅ English function names with Vietnamese data")
    print("✅ Clear architecture: Input -> Triage -> Patient Care -> (QA/Hospital/Dispatch)")
    print("✅ Real-time progress display")
    print("✅ Simple availability-based routing")
    print("")
    print("🌐 Starting web server...")
    print("📍 Access: http://localhost:5000")
    print("=" * 60)
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
