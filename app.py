from flask import Flask, request, jsonify
from twilio.twiml.voice_response import VoiceResponse
import threading
from services.phone_service import PhoneService
from services.dashboard_service import DashboardService, create_dashboard
from models.emergency_classifier import EmergencyClassifier
from config import Config
from datetime import datetime

app = Flask(__name__)

# Initialize services
phone_service = PhoneService()
dashboard_service = DashboardService()
classifier = EmergencyClassifier()

@app.route('/emergency-call', methods=['POST'])
def handle_emergency_call():
    """Handle incoming emergency calls"""
    response = phone_service.create_voice_response()
    return str(response)

@app.route('/process-emergency', methods=['POST'])
def process_emergency():
    """Process emergency speech input"""
    # Get speech result from Twilio
    speech_result = request.form.get('SpeechResult', '')
    caller_number = request.form.get('From', 'Unknown')
    call_sid = request.form.get('CallSid', 'Unknown')
    
    if speech_result:
        # Process with ML
        analysis = classifier.process_emergency_report(speech_result)
        
        # Add call metadata
        analysis.update({
            'caller_number': caller_number,
            'call_sid': call_sid,
            'timestamp': datetime.now().isoformat()
        })
        
        # Save to dashboard
        dashboard_service.add_emergency_report(analysis)
        
        # Save to file
        call_id = phone_service.save_emergency_call(analysis)
        
        # Respond to caller
        response = VoiceResponse()
        response.say(
            f"Thank you. Your emergency has been recorded and help is being dispatched. "
            f"Reference number: {call_id[:8]}. "
            f"Asante. Dharura yako imerekodiwa na msaada unakuja.",
            language='en'
        )
        
        return str(response)
    
    # No speech detected
    response = VoiceResponse()
    response.say("No emergency message received. Please call again if you need help.")
    return str(response)

@app.route('/dashboard-data', methods=['GET'])
def get_dashboard_data():
    """API endpoint for dashboard data"""
    return jsonify({
        'summary': dashboard_service.get_dashboard_summary(),
        'recent_emergencies': dashboard_service.emergency_data[-10:] if dashboard_service.emergency_data else []
    })

def run_dashboard():
    """Run the Gradio dashboard in a separate thread"""
    dashboard_app = create_dashboard()
    dashboard_app.launch(
        server_name=Config.DASHBOARD_HOST,
        server_port=Config.DASHBOARD_PORT,
        share=False
    )

if __name__ == '__main__':
    # Start dashboard in separate thread
    dashboard_thread = threading.Thread(target=run_dashboard)
    dashboard_thread.daemon = True
    dashboard_thread.start()
    
    # Start Flask app for phone service
    print("Starting Emergency Response System...")
    print(f"Phone service running on Flask")
    print(f"Dashboard available at http://localhost:{Config.DASHBOARD_PORT}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
