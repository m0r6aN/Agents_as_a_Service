
# **Agents as a Service (AaaS) Framework**

## Overview
Agents as a Service (AaaS) is a modular, agent-based framework designed to handle complex, multi-step processes using a variety of intelligent agents. Each agent is a self-contained unit, deployed in its own Docker container, capable of executing tasks, recalling memory, leveraging knowledge resources, and interacting with external systems. The framework is designed to scale, evolve, and adapt to various use cases like data ingestion, real-time notifications, and AI-driven decision-making.

AaaS leverages Kafka for communication between agents, enabling dynamic orchestration of tasks, logging, notifications, and monitoring via specialized agents. Whether it’s processing real-time data, handling exceptions, or sending notifications, AaaS is designed to be flexible, efficient, and scalable.
The Agents as a Service (AaaS) framework is designed to enable architects and developers to create and deploy multi-agent workflows in cloud environments like Google Cloud or Azure. The framework allows the orchestration of complex, multi-step processes using persistent, reusable agents.

## Why AaaS?
* **Smart Automation:** Self-orchestrating, intelligent, and cloud-agnostic—works seamlessly in any cloud environment.
* **Rapid Development:** Quickly design and implement custom workflows managed by 1 to n agents.
* **Modular & Reusable:** A modular architecture that enables reuse of agents and tools across projects.
* **Monitoring & Logging:** Comprehensive, built-in monitoring and logging for full process visibility.
* **Hybrid Architecture:** Combines Small and Large Language Models (SLM and LLM) with intelligent routing for optimal task execution.
* **Security First:** Secure ingress filtering to protect against prompt injection attacks.
* **Blazing Fast:** Prompt caching and parallel execution boost performance like a champ.
* **Highly Extensible:** Easily add new agents, tools, and features as your requirements evolve.
* **Asynchronous Execution:** Non-blocking, asynchronous task management for enhanced performance.
* **Consistent Deployment:** Dockerized architecture ensures easy and reliable deployments.
* **Scalable & Manageable:** Native Kubernetes support for seamless scaling and orchestration.
* **Resilient Execution:** Built-in retry logic ensures tasks are completed successfully, even in the event of failures.
* **State Management:** The ExecutionContext tracks process states, ensuring accurate task transitions, dependency management, and recovery from failures.
* **Persistent Agents:** Agents persist across workflows, allowing them to reuse knowledge and configurations from previous executions.
* **Dynamic Task Scheduling:** The Orchestrator dynamically schedules tasks based on dependencies, allowing for flexible and adaptable processes.

## **Features**
- **Agent-Centric Architecture**: Each agent lives in its own Docker container and can perform specialized tasks, process data, and store local memories.
- **Modular Design**: Agents can be dynamically assigned to processes based on task requirements, making the system highly flexible and scalable.
- **Built-In Knowledge Access**: Each agent has a knowledge folder for local files, augmenting the agent’s ability to perform tasks without re-training or fine-tuning.
- **Redis Cache & Long-Term Memory**: Agents maintain short-term memory via Redis and long-term memory in local SQLite databases for persistence.
- **Kafka-Driven Orchestration**: The Orchestrator agent dynamically assigns agents and tools, writing back to Kafka for execution.
- **Global Logging & Notifications**: Logging, error reporting, and notifications are handled by specialized agents that watch Kafka for events like task status, exceptions, and more.

## Process Execution

### 1. Task Assignment:

The Orchestrator parses tasks from the Process payload. If a Task does not have an Agent assigned to it, the Orchestrator will search the database for an Agent capable of fulfilling the task. It will also search the database for tools needed to perform a task, such as a web scraping script. If no tool exists, the Orchestrator will create one, persist it to the database, and assign it to the Agent.

### 2. Task Execution:

The Orchestrator directly executes tasks. It invokes the _execute_task_async() method on the agent, assigning tools as necessary for the task.

### 3. Retry Mechanism:

The Orchestrator handles retries in case of task failure, based on predefined retry logic. This ensures robustness and resiliency during execution.

### 4. Task Completion:

Upon successful task completion, the Agent reports the result back to Kafka. The ExecutionContext updates the state with the task result and reports it to the Orchestrator.

### 5. Next Task:

The Orchestrator checks the next task in the process, ensuring that any dependencies for the task are met before execution. This process continues until all tasks in the process are completed.

### 6. Parallel Execution
Each task may have 0-n dependencies (tasks that must be completed before they can start). If 2 or more tasks have no dependencies, the Orchestrator will execute them in parallel for optimal performance.

## Key Features
### 1. Dynamic Task Execution: 
Agents are dynamically assigned tasks based on the current state of the process, allowing for flexible, real-time task assignment.

### 2. Retry Mechanism: 
If a task fails, it is retried based on predefined conditions, ensuring that tasks are completed even in the event of failure.

### 3. Persistent Agents: 
Agents persist across multiple executions and can be reconfigured for new tasks, reducing the need to spin up new agents for each task.

### 4. State Management: 
The ExecutionContext tracks the progress of the process, ensuring accurate state transitions, task execution, and coordination with Kafka.

## **Data Schema**
Here’s a simplified look at the core data schema that drives the AaaS framework:

```json
{
  "process_id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Data Ingestion",
  "description": "Ingesting data from various sources",
  "tasks": [
    {
      "id": "423e4567-e89b-12d3-a456-426614174003",
      "name": "Extract Data",
      "dependencies": [],
      "agent": {
        "id": "323e4567-e89b-12d3-a456-426614174002",
        "name": "Data Agent",
        "model": {
          "id": "microsoft/Phi-3.5-mini-instruct",
          "inference_url": "https://phi-mini-instruct.model.com/api/v1/infer",
          "parameters": []
        },
        "tools": [
          {
            "id": "223e4567-e89b-12d3-a456-426614174001",
            "name": "ETL Tool"
          }
        ]
      }
    },
    {
      "id": "723e4567-e89b-12d3-a456-426614174006",
      "name": "Convert Results to HTML",
      "dependencies": [
        {
          "task_id": "423e4567-e89b-12d3-a456-426614174003"
        }
      ],
      "agent": {
        "id": "923e4567-e89b-12d3-a456-426614174008",
        "name": "HTML Conversion Agent",
        "model": {
          "id": "custom/html-conversion-model",
          "inference_url": "https://html-conversion.model.com/api/v1/convert",
          "parameters": []
        },
        "tools": [
          {
            "id": "b23e4567-e89b-12d3-a456-426614174010",
            "name": "HTML Converter"
          }
        ]
      }
    },
    {
      "id": "823e4567-e89b-12d3-a456-426614174007",
      "name": "Send Results via Email",
      "dependencies": [
        {
          "task_id": "723e4567-e89b-12d3-a456-426614174006"
        }
      ],
      "agent": {
        "id": "a23e4567-e89b-12d3-a456-426614174009",
        "name": "Email Agent",
        "model": {
          "id": "custom/email-sender-model",
          "inference_url": "https://email-sender.model.com/api/v1/send",
          "parameters": []
        },
        "tools": [
          {
            "id": "c23e4567-e89b-12d3-a456-426614174011",
            "name": "Email Sender"
          }
        ]
      }
    }
  ]
}
```

## **Architecture**
Each agent is containerized using Docker and includes:
- **Agent Code**: Custom logic for each agent’s tasks.
- **Knowledge Folder**: Local knowledge base for reference files.
- **Logs Directory**: Centralized logging for each agent.
- **Redis Cache**: Quick recall of frequently accessed data or recent requests.
- **Local Database (SQLite)**: Persistent long-term memory for storing task history, learned behaviors, etc.
- **Logging Configuration**: Managed via \`logging.config\`.
- **Requirements.txt**: Dependency management for the Docker container.

## **Future Development**

The AaaS framework is built to evolve. Here are some potential future development ideas:
- **Agent Marketplace**: Develop a marketplace for new agents, tools, and models that can be dynamically added into the system.
- **Distributed Long-Term Memory**: Move from local SQLite to a distributed database (e.g., PostgreSQL, NoSQL) for sharing knowledge across agents.
- **Advanced Monitoring & Analytics**: Implement centralized logging and monitoring with tools like the ELK stack (Elasticsearch, Logstash, Kibana) or Prometheus/Grafana for real-time metrics.
- **Auto Scaling with Kubernetes**: Introduce Kubernetes to auto-scale agent containers based on demand.
- **More Tools & Language Support**: Expand the types of tools available, supporting languages like JavaScript, Rust, or Go.
- **Enhanced RAG Integration**: Build out the "local RAG" knowledge access feature with more advanced retrieval and augmentation techniques.

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/agents_as_a_service.git
   cd agents_as_a_service
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the project in editable mode:
   ```
   pip install -e .
   ```

4. Install development dependencies:
   ```
   pip install -r requirements-dev.txt
   ```

## How to Run Tests
The project uses pytest and pytest-asyncio for testing the Orchestrator and TaskScheduler.

### 1. Run Tests:

```bash
pytest tests/core/test_orchestrator.py
```

### 2. Test Coverage:

The test suite covers the Orchestrator’s task execution, retry logic, and task sequencing based on dependencies.

## Docker Containerization

### Agents
Each Agent in AaaS should be containerized using Docker. Here's a basic `Dockerfile` template:

```dockerfile
# Use a Python base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
# ENV NAME World

# Run app.py when the container launches
CMD ["python", "orchestrator_agent.py"]
```

### Models
We can use a similar approach to deploy a fine-tuned model with an exposed API endpoint. This example uses a pre-trained model and CUDA enabled image.

```bash
# Use a base image with CUDA support
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common \
    build-essential \
    wget \
    git \
    libgl1-mesa-glx

# Add deadsnakes PPA for Python 3.12
RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.12 python3.12-distutils python3.12-dev python3-pip

# Set Python 3.12 as the default version of Python
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1

# Install pip for Python 3.12
RUN wget https://bootstrap.pypa.io/get-pip.py && python3.12 get-pip.py

# Set working directory
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the API port
EXPOSE 9000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "sql-nlp:app", "--host", "0.0.0.0", "--port", "9000"]
```

To build and run a Docker container for an agent or model:

1. Navigate to the process directory:
   ```
   cd agents/sql-nlp
   ```

2. Build the Docker image:
   ```
   docker build -t sql-nlp --cache-from sql-nlp .
   ```

3. Run the Docker container:
   ```
   docker run --gpus all -d -p 9000:9000 sql-nlp
   ```

### Verify GPU Usage: 
You can verify that PyTorch is using the GPU by running this command inside your FastAPI app or container:

```python
import torch
print(torch.cuda.is_available())  # Should print True if GPU is available
```

### Verify Python version:
You can verify that the correct Python version is running inside your Docker container by executing the following:
```bash
docker exec -it <container_id> python3 --version
```

## Kubernetes Deployment

AaaS processes can be deployed to Kubernetes for scalable and manageable operations. Here's a basic deployment template:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: aaas-process1
spec:
  replicas: 1
  selector:
    matchLabels:
      app: aaas-process1
  template:
    metadata:
      labels:
        app: aaas-process1
    spec:
      containers:
      - name: aaas-process1
        image: your-registry/aaas-process1:latest
        env:
        - name: CONFIG_PATH
          value: /app/config.py
```

To deploy a process to Kubernetes:

1. Ensure you have `kubectl` installed and configured.
2. Apply the deployment:
   ```
   kubectl apply -f kubernetes/process1/deployment.yaml
   ```

For more complex deployments, consider using Helm charts or Kubernetes Operators.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
