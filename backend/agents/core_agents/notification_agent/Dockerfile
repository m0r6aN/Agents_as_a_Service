# agents/core_agents/notification_agent/Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY ../../../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ../../../agents/ ./agents/
COPY ../../../messaging/ ./messaging/
COPY ../../../database/ ./database/
COPY notification_agent_main.py ./

CMD ["python", "notification_agent_main.py"]
