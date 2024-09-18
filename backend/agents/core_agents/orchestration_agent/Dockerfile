# agents/orchestrator/Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY ../../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ../../agents/ ./agents/
COPY ../../messaging/ ./messaging/
COPY ../../database/ ./database/
COPY ../../main.py ./

CMD ["python", "main.py"]

# Build the Docker image
# docker build -t orchestrator-agent -f agents/orchestrator/Dockerfile .

# Run the Docker container
# docker run -d --name orchestrator-agent orchestrator-agent