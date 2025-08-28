FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install system dependencies for audio and security updates
RUN apt-get update && apt-get install -y ffmpeg build-essential \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy .env file
COPY .env /app/.env

# Expose port (change if your app uses a different port)
EXPOSE 7860

# Run the app
CMD ["python", "app.py"]