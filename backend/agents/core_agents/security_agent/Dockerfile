# agents/core_agents/security_agent/Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY ../../../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ../../../agents/ ./agents/
COPY ../../../messaging/ ./messaging/
COPY ../../../database/ ./database/
COPY security_agent_main.py ./

CMD ["python", "security_agent_main.py"]
