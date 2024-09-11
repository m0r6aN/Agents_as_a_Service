# Agents as a Service (AaaS)

## Overview

The Agents as a Service (AaaS) framework is designed to enable architects and developers to create and deploy multi-agent workflows in cloud environments like Google Cloud or Azure. The framework allows the orchestration of complex, multi-step processes using persistent, reusable agents.

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
* Resilient Execution: TaskHandler with Retry Logic: Built-in retry logic ensures tasks are executed successfully even in the face of transient failures.
* State Management: Track the execution state of workflows with the ExecutionContext, enabling accurate task transitions and recovery from failures.
* Persistent Agents: Agents persist across processes, enabling them to reuse knowledge and configuration from previous executions.
* Orchestrated Workflows: Dynamic task scheduling based on task dependencies, allowing flexible and adaptable workflows.

## Key Components

AaaS provides several core components that can be extended and customized:

### 1. Orchestrator Agent:

The Orchestrator is responsible for managing the execution of tasks across multiple agents.
It dynamically decides the order in which tasks should be executed based on task dependencies.
It interfaces with the TaskHandler to execute tasks and manage retries.

### 2. TaskHandler:

The TaskHandler handles the execution of tasks delegated by the Orchestrator.
It encapsulates the task execution logic, including retry mechanisms.
It invokes the _execute_task_async() method on agents to perform the actual work, with the ability to retry on failure.

### 3. Process:

A Process defines the overall workflow and tasks involved.
Each process contains multiple tasks, with each task assigned to a specific agent.
The process also defines task dependencies, allowing the Orchestrator to execute tasks in the correct sequence.

### 4. ExecutionContext:

The ExecutionContext maintains the current state of task execution.
It stores the results of completed tasks and tracks which tasks have been successfully executed.
This context is passed between the Orchestrator and the agents to ensure the correct state is maintained throughout the workflow.


## Framework Architecture
The following diagram represents the high-level architecture of the Agents as a Service (AaaS) framework:

```lua
+-------------------+            +-------------------+            +-------------------+
|                   |            |                   |            |                   |
|     Orchestrator   |----------->|    TaskHandler    |----------->|       Agent        |
|                   |            |                   |            |                   |
+-------------------+            +-------------------+            +-------------------+
        |                                                        |
        |                                                        |
        +-----------------------> Process                        |
                                +-------------------+            |
                                |                   |            |
                                |  ExecutionContext |<------------+
                                |                   |
                                +-------------------+

```

This diagram illustrates the key components of the AaaS framework:
- The Orchestrator manages multiple Processes.
- Each Process consists of multiple Agents.
- All Agents utilize Core Components (Base Agent, System Messages, Prompts, Actions, and Tools).
- Monitoring and Logging Agents provide system-wide capabilities.
- Processes are containerized using Docker and can be deployed to a Kubernetes cluster.

## Workflow Execution

### 1. Task Assignment:

The Orchestrator retrieves the first task from the workflow and identifies the appropriate agent.

### 2. Task Execution:

The Orchestrator delegates the task execution to the TaskHandler.
The TaskHandler invokes the _execute_task_async() method on the agent.

### 3. Retry Mechanism:

The TaskHandler is responsible for retrying task execution in case of failure, based on predefined retry logic.
The retry mechanism ensures robustness and resiliency during execution.

### 4. Task Completion:

Upon successful task completion, the TaskHandler reports the result back to the Orchestrator.
The Orchestrator updates the ExecutionContext with the task result.

### 5. Next Task:

The Orchestrator checks the next task in the workflow, ensuring that any dependencies for the task are met before execution.
This process continues until all tasks in the workflow are completed.

## Key Features
### 1. Dynamic Task Execution: 
Agents are dynamically assigned tasks based on the current state of the workflow.

### 2. Retry Mechanism: 
If a task fails, it is retried based on predefined conditions.

### 3. Persistent Agents: 
Agents persist across multiple executions and can be reconfigured for new tasks.

### 4. State Management: 
The ExecutionContext tracks the progress of the workflow, ensuring accurate state transitions and task execution.

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

## How to Run Tests
The project uses pytest and pytest-asyncio for testing the Orchestrator and TaskHandler.

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

