# agents/core_agents/chat_agent/Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY ../../../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ../../../agents/ ./agents/
COPY ../../../messaging/ ./messaging/
COPY ../../../database/ ./database/
COPY chat_agent_main.py ./

CMD ["python", "chat_agent_main.py"]
