from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    # Twilio Configuration
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
    
    # Emergency Response Configuration
    EMERGENCY_HOTLINE = os.getenv('EMERGENCY_HOTLINE', '+254700000000')
    
    # Model Configuration
    WHISPER_MODEL = 'base'  # base model supports multilingual
    CLASSIFICATION_MODEL = 'microsoft/DialoGPT-medium'
    
    # Language Support
    SUPPORTED_LANGUAGES = ['en', 'sw']  # English and Swahili
    
    # Dashboard Configuration
    DASHBOARD_PORT = 7860
    DASHBOARD_HOST = '0.0.0.0'
    
    # Database (simple file-based for this example)
    DATA_DIR = 'emergency_data'
    AUDIO_DIR = 'audio_files'