def detect_language(text: str) -> str:
    """Simple language detection for Swahili vs English"""
    swahili_indicators = [
        'ni', 'na', 'wa', 'ya', 'za', 'la', 'pa', 'kwa', 'katika', 
        'mimi', 'wewe', 'yeye', 'sisi', 'ninyi', 'wao',
        'dharura', 'msaada', 'polisi', 'hospitali', 'daktari'
    ]
    
    text_lower = text.lower()
    swahili_count = sum(1 for word in swahili_indicators if word in text_lower)
    
    # Simple heuristic: if more than 2 Swahili indicators, classify as Swahili
    return 'sw' if swahili_count > 2 else 'en'

def get_response_text(message_key: str, language: str = 'en') -> str:
    """Get localized response text"""
    responses = {
        'greeting': {
            'en': "Emergency hotline. Please describe your emergency.",
            'sw': "Huduma ya dharura. Tafadhali eleza dharura yako."
        },
        'confirmation': {
            'en': "Thank you. Your emergency has been recorded and help is being dispatched.",
            'sw': "Asante. Dharura yako imerekodiwa na msaada unakuja."
        },
        'no_input': {
            'en': "We didn't receive your message. Please call again.",
            'sw': "Hatukupokea ujumbe wako. Tafadhali piga simu tena."
        }
    }
    
    return responses.get(message_key, {}).get(language, responses[message_key]['en'])
