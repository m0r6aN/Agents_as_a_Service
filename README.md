# Agents as a Service (AaaS)

## Overview

Agents as a Service (AaaS) is your go-to solution for automating processes with the power of specialized AI agents. This system offers unparalleled flexibility and scalability, making it a breeze to design and deploy complex workflows by seamlessly orchestrating multiple agents, each laser-focused on their part of the process.

## Why AaaS?
* Smart Automation: Self-orchestrated, intelligent, and works in any cloud environment.
* Rapid Development: Quickly design and implement custom processes handled by 1 to n agents.
* Modular & Reusable: A modular architecture with core components you can reuse across projects.
* Monitoring & Logging: Keep tabs on everything with built-in monitoring and logging.
* Hybrid Architecture: Combines SLM and LLM with intelligent routing.
* Security First: Secure ingress filtering to thwart prompt injection attacks.
* Blazing Fast: Prompt caching boosts performance like a champ.
* Highly Extensible: Easily add new agents and functionalities as your needs evolve.
* Asynchronous Execution: Boost performance with non-blocking, asynchronous operations.
* Consistent Deployment: Dockerized for easy and reliable deployment.
* Scalable & Manageable: Kubernetes support for deployment at scale with minimal fuss.

## Table of Contents

1. [Core Components](#core-components)
2. [Framework Architecture](#framework-architecture)
3. [Project Structure](#project-structure)
4. [Setup](#setup)
5. [Usage](#usage)
6. [Creating a New Process](#creating-a-new-process)
7. [Core Components](#core-components)
8. [Docker Containerization](#docker-containerization)
9. [Kubernetes Deployment](#kubernetes-deployment)
10. [Contributing](#contributing)
11. [License](#license)

## Core Components

AaaS provides several core components that can be extended and customized:

- **Agents**: Base classes for creating specialized agents.
- **System Messages**: Predefined messages for agent communication.
- **Prompts**: Templates for generating queries or instructions.
- **Actions**: Reusable functions that agents can perform.
- **Tools**: Utility functions for common tasks.

Refer to the files in the `core/` directory for more details on each component.


## Framework Architecture
The following diagram represents the high-level architecture of the Agents as a Service (AaaS) framework:

[Insert the Mermaid diagram here]

This diagram illustrates the key components of the AaaS framework:
- The Orchestrator manages multiple Processes.
- Each Process consists of multiple Agents.
- All Agents utilize Core Components (Base Agent, System Messages, Prompts, Actions, and Tools).
- Monitoring and Logging Agents provide system-wide capabilities.
- Processes are containerized using Docker and can be deployed to a Kubernetes cluster.


## Project Structure

```
agents_as_a_service/
├── core/
│   ├── agents/
│   │   ├── base.py
│   │   ├── monitoring_agent.py
│   │   └── logging_agent.py
│   ├── system_messages/
│   │   ├── base_messages.py
│   │   └── specialized_messages.py
│   ├── prompts/
│   │   ├── base_prompts.py
│   │   └── specialized_prompts.py
│   ├── actions/
│   │   ├── file_actions.py
│   │   └── data_actions.py
│   ├── tools/
│   │   ├── file_utils.py
│   │   └── data_processing.py
│   ├── process.py
│   └── orchestrator.py
├── processes/
│   ├── process1/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── .dockerignore
│   │   ├── config.py
│   │   ├── custom_agents.py
│   │   ├── process.py
│   │   └── main.py
│   └── process2/
│       └── ...
├── kubernetes/
│   ├── process1/
│   │   └── deployment.yaml
│   └── process2/
│       └── deployment.yaml
├── tests/
├── setup.py
├── pyproject.toml
├── requirements.txt
└── README.md
```

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

## Usage

Here's a basic example of how to use the framework:

```python
import asyncio
from agents_as_a_service.core.orchestrator import OrchestratorAgent
from agents_as_a_service.processes.process1.process import Process1
from agents_as_a_service.processes.process1.config import PROCESS_CONFIG

async def main():
    process = Process1(PROCESS_CONFIG)
    orchestrator = OrchestratorAgent(process.agents)
    result = await orchestrator.execute(process.workflow, {})
    print(f"Process completed. Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Creating a New Process

To create a new process:

1. Create a new directory under `processes/` for your process.
2. Create the following files in your process directory:
   - `config.py`: Process configuration
   - `custom_agents.py`: Custom agents specific to your process
   - `process.py`: Process definition
   - `main.py`: Entry point for running the process
   - `Dockerfile`: For containerization
   - `requirements.txt`: Process-specific dependencies

3. Define your custom agents in `custom_agents.py`:

```python
from agents_as_a_service.core.agents.base import BaseAgent

class MyCustomAgent(BaseAgent):
    def __init__(self, config):
        super().__init__("My Custom Agent", "Performs a custom task")
        self.config = config

    async def execute(self, input_data):
        # Implement your agent logic here
        return {"result": "Custom task completed"}
```

4. Define your process in `process.py`:

```python
from agents_as_a_service.core.process import ProcessBase
from .custom_agents import MyCustomAgent

class MyCustomProcess(ProcessBase):
    def __init__(self, config):
        super().__init__("My Custom Process", "Performs a custom workflow", config)
        self.define_agents()
        self.define_workflow()

    def define_agents(self):
        self.add_agent(MyCustomAgent(self.config))

    def define_workflow(self):
        self.set_workflow({
            "tasks": {
                "custom_task": {"agent": "MyCustomAgent", "dependencies": ["monitoring", "logging"]}
            }
        })
```

## Docker Containerization

Each process in AaaS can be containerized using Docker. Here's a basic `Dockerfile` template:

```dockerfile
FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

To build and run a Docker container for a process:

1. Navigate to the process directory:
   ```
   cd processes/process1
   ```

2. Build the Docker image:
   ```
   docker build -t aaas-process1 .
   ```

3. Run the Docker container:
   ```
   docker run aaas-process1
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

