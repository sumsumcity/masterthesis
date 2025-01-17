FROM python:3.10-slim

# Arbeitsverzeichnis
WORKDIR /app

# Abhängigkeiten installieren
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Flask-App kopieren
COPY . .

# Flask starten
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]