# 🏥 Patient Dispatch System

Vietnamese Patient Dispatch System with Real-time Workflow Tracking

## 🌟 Features

- **English Function Names** with Vietnamese data support
- **Real-time Progress Tracking** via SocketIO
- **Clean Architecture**: Input → Triage → Patient Care → (QA/Hospital/Dispatch)
- **Simple Availability-based Routing** (no complex logic)
- **Mock Data** for hospitals, ambulances, and medical staff
- **Responsive Web Interface** with Bootstrap

## 🏗️ Architecture

```
Input → Triage Agent → Patient Care Agent → Final Routing
                                         ├── QA Consultation (Priority 1-2)
                                         ├── Hospital Direct (Priority 3-4)  
                                         └── Emergency Dispatch (Priority 5)
```

## 📋 Workflow Steps

1. **Information Extraction** - Analyze patient description and symptoms
2. **Triage Assessment** - Calculate priority score (1-5) and urgency level
3. **Routing Decision** - Determine appropriate care pathway
4. **Execute Routing** - Route to QA/Hospital/Emergency services
5. **Final Optimization** - Optimize assignment and provide backup options

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Flask, Flask-SocketIO
- Modern web browser

### Installation

1. Clone the repository:
```bash
git clone https://github.com/ShouyiLeee/patient-dispatch-system.git
cd patient-dispatch-system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env file with your API keys (optional for mock mode)
```

4. Run the application:
```bash
python app_simple_working.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## 🧪 Testing

### Run Workflow Test
```bash
python test_clean_workflow.py
```

This will test the complete workflow with 3 scenarios:
- Normal patient (→ QA Consultation)
- Urgent patient (→ Hospital Direct)
- Emergency patient (→ Emergency Dispatch)

## 💻 Usage

### Web Interface

1. **Patient Input Form**:
   - Enter patient description
   - Input vital signs (heart rate, blood pressure, SpO2, temperature)
   - Click "Bắt đầu Điều phối" to start workflow

2. **Quick Test Cases**:
   - Use predefined test cases for different patient types
   - One-click testing for normal/urgent/emergency scenarios

3. **Real-time Progress**:
   - Watch 5-step workflow progress in real-time
   - Visual indicators for each processing step
   - Final routing result with detailed information

4. **QA Chat** (if routed to consultation):
   - Interactive chat with medical expert
   - Context-aware responses
   - Seamless conversation flow

### API Endpoints

- `GET /` - Main web interface
- `POST /api/process_patient` - Start patient workflow
- `POST /api/qa_chat` - QA consultation chat
- `GET /api/test_cases` - Get predefined test cases

### WebSocket Events

- `workflow_start` - Workflow initialization
- `workflow_progress` - Step-by-step progress updates
- `workflow_complete` - Final result
- `workflow_error` - Error handling

## 📊 Patient Priority Scoring

| Priority | Level | Action | Examples |
|----------|-------|--------|----------|
| 1-2 | Normal | QA Consultation | Mild fever, cough |
| 3-4 | Urgent | Hospital Direct | Severe pain, vomiting |
| 5 | Emergency | Dispatch + Hospital | Chest pain, difficulty breathing |

## 🏥 Mock Data

### Hospitals
- Bệnh viện Chớ Rẫy (2.5km, 85% capacity)
- Bệnh viện Đại học Y Dược (3.2km, 70% capacity)

### Ambulances
- Type A Emergency (CC01, 1.5km, 4min ETA)
- Type B Standard (CC02, 2.1km, 5min ETA)
- Pediatric Ambulance (CC03, 3.0km, 7min ETA)

### Medical Staff
- Doctors: BS. Nguyễn Văn An, BS. Trần Thị Bình, etc.
- Paramedics: Nguyễn Văn Cường, Trần Thị Dung, etc.

## 🛠️ Development

### Project Structure
```
patient-dispatch-system/
├── app_simple_working.py          # Main Flask application
├── test_clean_workflow.py         # Workflow testing
├── templates/
│   └── simple_working_interface.html
├── modules/                       # Core modules
│   ├── gemini_client.py
│   ├── triage_module/
│   ├── patient_care_module/
│   └── flow_optimizer_module/
├── data/                          # JSON data files
├── config/                        # Configuration
└── requirements.txt
```

### Key Components

1. **SimplePatientDispatchWorkflow** - Main workflow orchestrator
2. **Mock Agents** - Simplified agents for testing
3. **Real-time Updates** - SocketIO integration
4. **Responsive UI** - Bootstrap-based interface

### Adding New Features

1. **New Agent**: Add to `test_clean_workflow.py`
2. **New UI Component**: Modify `simple_working_interface.html`
3. **New API Endpoint**: Add to `app_simple_working.py`
4. **New Mock Data**: Update respective mock classes

## 🔧 Configuration

### Environment Variables (.env)
```bash
# API Keys (optional for mock mode)
GOOGLE_AI_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# Flask Settings
FLASK_ENV=development
FLASK_DEBUG=True
```

### Runtime Settings
- Port: 5000
- Host: 0.0.0.0 (all interfaces)
- Debug: True (development mode)

## 🚨 Error Handling

- **Import Errors**: Graceful fallback to mock agents
- **API Failures**: Default responses with error logging
- **Workflow Errors**: Safe routing to QA consultation
- **Socket Disconnection**: Automatic reconnection attempts

## 📝 Logging

- **Console Output**: Real-time workflow progress
- **File Logging**: Detailed debug information
- **Error Tracking**: Exception handling and reporting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with Flask and Socket.IO
- UI components from Bootstrap
- Vietnamese language support
- Real-time progress tracking

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the console logs for debugging
- Test with provided mock scenarios

---

**Status**: ✅ Working and Tested  
**Last Updated**: June 12, 2025  
**Version**: 1.0.0