# EveShield Emergency Response System

## Overview

**EveShield** is an emergency response platform designed to help users report emergencies, trigger SOS alerts, track their location, and maintain a trauma journal. It integrates voice call handling, machine learning for emergency classification, multilingual transcription, and a dashboard for monitoring incidents.

## Features

- **Emergency Hotline**: Receives and processes emergency voice calls via Twilio.
- **SOS Trigger**: Allows users to send instant SOS alerts.
- **GPS Tracking**: Users can share their location during emergencies.
- **Trauma Journal**: Users can record their experiences.
- **Dashboard**: Visualizes recent emergencies and system status.
- **Multilingual Support**: English and Swahili.

## Tech Stack

- **Backend**: Python, Flask, Twilio, Gradio, Whisper, Transformers
- **Frontend**: HTML, CSS, JavaScript, Express.js
- **Machine Learning**: Emergency classification, speech transcription
- **Containerization**: Docker

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js (for frontend)
- Docker (optional)
- Twilio account (for voice calls)

### Setup

1. **Clone the repository**

   ```sh
   git clone <repo-url>
   cd EveShield
   ```

2. **Install Python dependencies**

   ```sh
   python3 -m venv env
   source env/bin/activate
   python setup.py
   ```

3. **Configure environment variables**

   - Copy `.env.example` to `.env` and fill in your Twilio credentials.

4. **Run the backend**

   ```sh
   python app.py
   ```

   - Flask API runs on port 5000.
   - Gradio dashboard runs on port 7860.

5. **Run the frontend**

   ```sh
   cd Frontend
   npm install
   node server.js
   ```

   - Frontend runs on port 5000.

6. **Using Docker (optional)**
   ```sh
   docker build -t eveshield .
   docker run -p 7860:7860 -p 5000:5000 eveshield
   ```

### Twilio Webhook Setup

- Point your Twilio voice webhook to `/emergency-call` endpoint of your backend server.

## Project Structure

See below for a summary of key files and directories:

- [`app.py`](app.py): Main Flask backend.
- [`config.py`](config.py): Configuration and environment variables.
- [`services/phone_service.py`](services/phone_service.py): Handles Twilio calls and transcription.
- [`models/emergency_classifier.py`](models/emergency_classifier.py): ML emergency classifier.
- [`Frontend/index.html`](Frontend/index.html): Main frontend UI.
- [`Frontend/script.js`](Frontend/script.js): Frontend logic.
- [`Frontend/server.js`](Frontend/server.js): Express.js server for frontend.
- [`requirements.txt`](requirements.txt): Python dependencies.
- [`Dockerfile`](Dockerfile): Containerization setup.

## Contributing

1. Fork the repo and create your branch.
2. Follow the setup instructions above.
3. Make your changes and submit a pull request.
4. Ensure your code is well-documented and tested.

## Contact

For questions or support, open an issue or contact the maintainers.
