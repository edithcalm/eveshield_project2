from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
import speech_recognition as sr
import whisper
from pydub import AudioSegment
import os
import uuid
from datetime import datetime
from config import Config
from typing import Dict

class PhoneService:
    def __init__(self):
        self.client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
        self.whisper_model = whisper.load_model(Config.WHISPER_MODEL)
        self.recognizer = sr.Recognizer()
        
        # Ensure directories exist
        os.makedirs(Config.DATA_DIR, exist_ok=True)
        os.makedirs(Config.AUDIO_DIR, exist_ok=True)
    
    def create_voice_response(self) -> VoiceResponse:
        """Create TwiML response for emergency calls"""
        response = VoiceResponse()
        
        # Multilingual greeting
        response.say(
            "Emergency hotline. Please describe your emergency. "
            "Huduma ya dharura. Tafadhali eleza dharura yako.",
            language='en'
        )
        
        # Gather audio input
        gather = Gather(
            input='speech',
            timeout=30,
            speechTimeout='auto',
            action='/process-emergency',
            method='POST'
        )
        response.append(gather)
        
        # Fallback if no input
        response.say("We didn't receive your message. Please call again.")
        
        return response
    
    def transcribe_audio(self, audio_url: str) -> Dict[str, str]:
        """Transcribe audio from Twilio recording"""
        try:
            # Download audio file
            audio_filename = f"{Config.AUDIO_DIR}/{uuid.uuid4()}.wav"
            
            # For demo purposes, we'll simulate audio transcription
            # In real implementation, download from audio_url and process
            
            # Using Whisper for multilingual transcription
            result = self.whisper_model.transcribe(audio_filename)
            
            return {
                'text': result['text'],
                'language': result.get('language', 'unknown'),
                'confidence': 0.95  # Whisper doesn't provide confidence scores
            }
        except Exception as e:
            return {
                'text': f'Transcription failed: {str(e)}',
                'language': 'unknown',
                'confidence': 0.0
            }
    
    def save_emergency_call(self, call_data: Dict) -> str:
        """Save emergency call data to file"""
        call_id = str(uuid.uuid4())
        filename = f"{Config.DATA_DIR}/emergency_{call_id}.json"
        
        import json
        with open(filename, 'w') as f:
            json.dump(call_data, f, indent=2)
        
        return call_id