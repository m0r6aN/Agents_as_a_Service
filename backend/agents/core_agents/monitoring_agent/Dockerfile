# agents/core_agents/monitoring_agent/Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY ../../../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ../../../agents/ ./agents/
COPY ../../../messaging/ ./messaging/
COPY ../../../database/ ./database/
COPY monitoring_agent_main.py ./

CMD ["python", "monitoring_agent_main.py"]
