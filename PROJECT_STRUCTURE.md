# Patient Flow Coordination System - Project Structure

## Main Application Files
- `web_app_refactored.py` - Main refactored Flask application
- `web_app.py` - Original Flask application (legacy)
- `requirements.txt` - Python dependencies
- `.env` - Environment variables configuration
- `README.md` - Project documentation

## Core Modules
- `modules/` - Main application modules
  - `api_service.py` - Centralized API service
  - `config_service.py` - Configuration management
  - `workflow_service.py` - Workflow orchestration
  - `triage_module/` - Medical triage functionality
  - `patient_care_module/` - Patient care and chatbot
  - `hospital_coordination_module/` - Hospital matching and coordination
  - `flow_optimizer_module/` - Flow optimization

## Configuration & Data
- `config/` - Configuration files
- `data/` - Data files and examples
- `flow_logs/` - Flow execution logs and results

## Web Interface
- `templates/` - HTML templates
- `static/` - CSS, JS, and static assets

## Support Files
- `agents/` - Legacy agent implementations
- `db/` - Database models and utilities
- `tests/` - Test files
- `utils/` - Utility functions

## Usage
To run the refactored application:
```bash
python web_app_refactored.py
```

To run the original application:
```bash
python web_app.py
```

## Features
- Multi-agent patient flow coordination
- Real-time workflow tracking with SocketIO
- Medical image analysis with Google Gemini
- Hospital matching and optimization
- Interactive dashboard and reporting
- Chatbot interface for patient interaction
