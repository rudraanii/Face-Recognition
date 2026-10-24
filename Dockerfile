# Containerized environment for Face Recognition Attendance System
FROM python:3.10-slim

# Install system dependencies for Tkinter, OpenCV, and X11 virtual display
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-tk \
    libgl1 \
    libglib2.0-0 \
    xvfb \
    x11vnc \
    novnc \
    websockify \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose noVNC web port for browser access
EXPOSE 8080

# Start script running Xvfb virtual frame buffer, VNC server, noVNC, and the application
CMD ["sh", "-c", "Xvfb :0 -screen 0 1366x768x16 & export DISPLAY=:0 && x11vnc -display :0 -forever -nopw -listen localhost -xkb & websockify --web /usr/share/novnc 8080 localhost:5900 & python run.py"]
