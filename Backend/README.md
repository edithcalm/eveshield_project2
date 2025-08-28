# Eve Shield – Backend API

Eve Shield is a safety-first backend system built with Django & Django REST Framework to support a smart bracelet and mobile app platform focused on personal safety, emergency response, and legal/GBV support for underserved communities.

---

## 📁 Project Structure

The codebase is structured **by feature**, where each module (e.g. Tracking, Triggering, Onboarding) is developed as a self-contained Django app:

```
eve_shield/
├── config/                    # Django settings, URLs, and WSGI/ASGI configs
│
├── onboarding/               # User onboarding: contacts, permissions, policies
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
│
├── trigger/                  # SOS alerts, gestures, audio capture, power-off lock
│   ├── models.py
│   ├── views.py
│   ├── services/
│   └── urls.py
│
├── tracking/                 # GPS tracking, cell tower triangulation, etc.
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── resources/                # GBV resources, chatbot, trauma journal, legal aid
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── users/                    # Custom User model and auth logic
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── manage.py
└── requirements.txt
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-org>/eve-shield-backend.git
cd eve-shield-backend
```

### 2. Set up a virtual environment

MacOs/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv/Scripts/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up the database and make model migrations

```bash
python manage.py migrate
```

```bash
python manage.py makemigrations
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

You can now access the API at: `http://localhost:8000/api/`

You can now access the API at: `http://localhost:8000/api/`

---

## 📡 API Design Overview

All endpoints are under the `/api/` prefix. Auth is handled via JWT.

### 🔐 Auth

- `POST /api/users/auth/register/`
- `POST /api/users/auth/login/`
- `POST /api/users/auth/logout/`

For further Authentication Description:
[Authentication Guide](/Backend/authentication_guide.md)

### 👤 Onboarding

- `POST /api/onboarding/emergency-contact/` – add contact
- `GET /api/onboarding/policy/` – retrieve app policy
- `POST /api/onboarding/permissions/` – request app permissions

### 🚨 Trigger

- `POST /api/trigger/sos/` – trigger emergency alert
- `POST /api/trigger/gesture/` – submit panic gesture
- `POST /api/trigger/audio/` – upload voice note
- `POST /api/trigger/power-lock/` – enable screen blackout

### 📍 Tracking

- `POST /api/tracking/gps/` – submit current GPS coords
- `POST /api/tracking/cell/` – submit cell tower data
- `GET /api/tracking/pin-location/` – get pinned location

### 📘 Resources

- `GET /api/resources/gbv/` – fetch list of GBV help resources
- `POST /api/resources/journal/` – submit trauma report
- `POST /api/resources/chatbot/` – send message to assistant
- `GET /api/resources/legal-aid/` – find legal assistance

---

## 🧪 Testing

Use `pytest` or Django's default test runner:

```bash
python manage.py test
```

Each app contains its own `tests/` directory and should maintain full test coverage.

---

## 👥 Contributing

1. Fork the repository
2. Create a feature branch (`feature/your-feature`)
3. Add unit tests for any new functionality
4. Submit a pull request

---

## 🧭 Notes for New Developers

- Keep feature logic encapsulated in its app (don’t cross-import models or services between apps).
- DRF is used for all APIs — serializers go in `serializers.py`, views in `views.py`.
- Use the `services/` folder inside an app if logic gets bulky (e.g. audio processing, GPS parsing).
- Follow PEP8 and keep endpoints RESTful.

---

## 📌 Tech Stack

- **Python 3.11+**
- **Django 4+**
- **Django REST Framework**
- PostgreSQL (or SQLite during dev)
- JWT Authentication

---
