import torch
from transformers import (
    AutoTokenizer, AutoModelForSequenceClassification, 
    AutoModelForCausalLM, pipeline
)
from typing import Dict, List, Tuple
import re

class EmergencyClassifier:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Load multilingual models that support Swahili and English
        self.tokenizer = AutoTokenizer.from_pretrained('microsoft/DialoGPT-medium')
        self.summarizer = pipeline(
            'summarization', 
            model='facebook/bart-large-cnn',
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Classification pipeline for emergency types
        self.classifier = pipeline(
            'text-classification',
            model='cardiffnlp/twitter-roberta-base-emotion',
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Define emergency categories
        self.emergency_types = {
            'medical': ['hospital', 'doctor', 'sick', 'injured', 'ambulance', 'pain', 'bleeding',
                       'daktari', 'mgonjwa', 'hospitali', 'ambulensi', 'umwagika', 'maumivu'],
            'fire': ['fire', 'smoke', 'burning', 'flame', 'moto', 'moshi'],
            'crime': ['robbery', 'theft', 'attack', 'violence', 'police', 
                     'wizi', 'polisi', 'shambulio', 'jeuri'],
            'accident': ['accident', 'crash', 'collision', 'vehicle', 'ajali', 'gari'],
            'natural_disaster': ['flood', 'earthquake', 'storm', 'mafuriko', 'tetemeko']
        }
        
    def classify_emergency_type(self, text: str) -> str:
        """Classify the type of emergency based on keywords"""
        text_lower = text.lower()
        
        for emergency_type, keywords in self.emergency_types.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return emergency_type
        
        return 'general'
    
    def extract_location(self, text: str) -> str:
        """Extract location information from text"""
        # Simple location extraction - can be improved with NER models
        location_patterns = [
            r'at\s+([A-Za-z\s]+)',
            r'in\s+([A-Za-z\s]+)',
            r'near\s+([A-Za-z\s]+)',
            r'kwa\s+([A-Za-z\s]+)',  # Swahili
            r'karibu na\s+([A-Za-z\s]+)',  # Swahili
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return 'Location not specified'
    
    def generate_summary(self, text: str) -> str:
        """Generate a summary of the emergency report"""
        try:
            if len(text) < 50:
                return text
            
            summary = self.summarizer(text, max_length=100, min_length=20, do_sample=False)
            return summary[0]['summary_text']
        except Exception as e:
            return f"Summary generation failed: {str(e)}"
    
    def analyze_severity(self, text: str) -> str:
        """Analyze the severity of the emergency"""
        urgent_keywords = [
            'urgent', 'emergency', 'dying', 'dead', 'serious', 'critical',
            'haraka', 'dharura', 'mkuu', 'hatari'  # Swahili urgent terms
        ]
        
        text_lower = text.lower()
        for keyword in urgent_keywords:
            if keyword in text_lower:
                return 'HIGH'
        
        return 'MEDIUM'
    
    def process_emergency_report(self, text: str) -> Dict:
        """Process complete emergency report"""
        return {
            'original_text': text,
            'summary': self.generate_summary(text),
            'emergency_type': self.classify_emergency_type(text),
            'location': self.extract_location(text),
            'severity': self.analyze_severity(text),
            'recommended_actions': self.get_recommended_actions(
                self.classify_emergency_type(text),
                self.analyze_severity(text)
            )
        }
    
    def get_recommended_actions(self, emergency_type: str, severity: str) -> List[str]:
        """Get recommended actions based on emergency type and severity"""
        base_actions = {
            'medical': [
                'Dispatch ambulance immediately',
                'Contact nearest hospital',
                'Gather medical history if possible',
                'Provide first aid instructions if trained personnel available'
            ],
            'fire': [
                'Alert fire department',
                'Evacuate surrounding areas',
                'Check for casualties',
                'Ensure water supply access for firefighters'
            ],
            'crime': [
                'Dispatch police units',
                'Secure the area',
                'Interview witnesses',
                'Preserve evidence'
            ],
            'accident': [
                'Send emergency responders',
                'Clear traffic if road accident',
                'Check for injuries',
                'Contact relevant authorities'
            ],
            'natural_disaster': [
                'Activate emergency protocols',
                'Coordinate with disaster management',
                'Evacuate if necessary',
                'Provide emergency supplies'
            ],
            'general': [
                'Assess situation',
                'Dispatch appropriate responders',
                'Maintain communication with caller',
                'Document incident details'
            ]
        }
        
        actions = base_actions.get(emergency_type, base_actions['general'])
        
        if severity == 'HIGH':
            actions.insert(0, '⚠️ URGENT: Immediate response required')
        
        return actions
