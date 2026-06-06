# Production Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Install Ollama locally for the container
RUN curl -L https://ollama.com/install.sh | sh

CMD ["python", "src/alert_engine/stream_router.py"]
