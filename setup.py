import os
import subprocess
import sys
import shutil

def setup_project():
    """Setup the emergency response bot project"""

    print("Setting up Emergency Response Bot...")

    # Create necessary directories
    directories = ['emergency_data', 'audio_files', 'logs', 'services', 'models']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

    # Install requirements
    print("Installing Python packages...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

    # Create .env file from example
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            shutil.copy('.env.example', '.env')
            print("Created .env file from .env.example")
            print("Please update .env file with your actual credentials")
        else:
            print("Please create .env file with your Twilio credentials")

    print("Setup complete!")
    print("To run the system:")
    print("1. Update .env file with your credentials")
    print("2. Run: python app.py")
    print("3. Configure Twilio webhook to point to your /emergency-call endpoint")

if __name__ == '__main__':
    setup_project()