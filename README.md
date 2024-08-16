# Multi-Agent Framework for Process Automation

## Overview

This Multi-Agent Framework is a flexible and extensible system designed for process automation using a combination of specialized agents. It allows for the creation of complex workflows by orchestrating multiple agents, each responsible for specific tasks within a process.

Key features:
- Modular architecture with reusable core components
- Customizable processes with specific agents and workflows
- Built-in monitoring and logging capabilities
- Extensible design for adding new agents and functionalities
- Asynchronous execution for improved performance

## Table of Contents

1. [Framework Structure](#framework-structure)
2. [Setup](#setup)
3. [Usage](#usage)
4. [Creating a New Process](#creating-a-new-process)
5. [Core Agents](#core-agents)
6. [Extending the Framework](#extending-the-framework)
7. [Contributing](#contributing)
8. [License](#license)

## Framework Structure

```
multi_agent_framework/
├── core/
│   ├── agents/
│   │   ├── base.py
│   │   ├── monitoring_agent.py
│   │   └── logging_agent.py
│   ├── process.py
│   └── orchestrator.py
├── processes/
│   └── file_processing/
│       ├── config.py
│       ├── custom_agents.py
│       ├── process.py
│       └── main.py
├── tests/
├── setup.py
└── requirements.txt
```

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/multi-agent-framework.git
   cd multi-agent-framework
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Install the framework in editable mode:
   ```
   pip install -e .
   ```

## Usage

Here's a basic example of how to use the framework:

```python
import asyncio
from multi_agent_framework.core.orchestrator import OrchestratorAgent
from processes.file_processing.process import FileProcessingProcess
from processes.file_processing.config import PROCESS_CONFIG

async def main():
    # Create a process instance
    process = FileProcessingProcess(PROCESS_CONFIG)
    
    # Create an orchestrator with the process agents
    orchestrator = OrchestratorAgent(process.agents)
    
    # Execute the process
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

3. Define your custom agents in `custom_agents.py`:

```python
from multi_agent_framework.core.agents.base import BaseAgent

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
from multi_agent_framework.core.process import ProcessBase
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

5. Implement the main execution in `main.py`.

## Core Agents

The framework provides two core agents that are automatically included in every process:

1. **MonitoringAgent**: Monitors system resources (CPU, memory, disk usage).
2. **LoggingAgent**: Provides centralized logging for the entire process.

These agents are automatically added to your process and included in the workflow.

## Extending the Framework

To extend the framework:

1. Add new core agents in `multi_agent_framework/core/agents/`.
2. Create new base classes for different types of agents or processes in the core module.
3. Implement new utility functions or tools in the core module that can be used across different processes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

