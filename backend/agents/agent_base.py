# agents/agent_base.py

import importlib
import os
import sys
from typing import Any, Dict, List
import uuid
import logging
from abc import ABC, abstractmethod
import json
import csv
import pandas as pd
from PyPDF2 import PdfReader
import yaml
from agents.specialized_agents.specialized_agent import SpecializedAgent
from messaging.messaging import MessagingClient
from database.database_setup import Database

class Agent(ABC):
    def __init__(self, agent_name: str, system_message: str, model_name: str, tools: List[str] = None, memory: Dict[str, Any] = None, config: Dict[str, Any] = None):
        self.agent_id = str(uuid.uuid4())
        self.agent_name = agent_name
        self.system_message = system_message
        self.model_name = model_name
        self.tools = tools or []
        self.memory = memory or {}
        self.config = config or {}
        self.knowledge: Dict[str, Any] = self.load_knowledge()
        self.logger = logging.getLogger(self.agent_name)
        self.messaging_client = MessagingClient()
        self.db = Database()
        self.persist_agent()

    def persist_agent(self) -> None:
        agent_data = {
            'agent_id': self.agent_id,
            'agent_name': self.agent_name,
            'system_message': self.system_message,
            'model_name': self.model_name,
            'tools': self.tools,
            'memory': self.memory,
            'config': self.config
        }
        self.db.save_agent(agent_data)
        self.logger.debug(f"Agent {self.agent_id} persisted to database.")

    @abstractmethod
    def perform_task(self, task):
        pass
    
    def change_model(self, new_model_name: str) -> None:
        self.model_name = new_model_name
        self.logger.info(f"Model changed to {new_model_name}")
        self.persist_agent()
        
    def add_tool(self, tool: str) -> None:
        self.tools.append(tool)
        self.logger.info(f"Tool added: {tool}")
        self.persist_agent()
        
    def remove_tool(self, tool: str) -> None:
        if tool in self.tools:
            self.tools.remove(tool)
            self.logger.info(f"Tool removed: {tool}")
            self.persist_agent() 
            
    def create_and_execute_tool(self, tool_name: str, tool_description: str, code: str, *args, **kwargs):
        tool_id = self.create_tool(tool_name, tool_description, code)
        return self.execute_tool(tool_id, *args, **kwargs)

    def create_tool(self, tool_name: str, tool_description: str, code: str) -> str:
        tool_id = str(uuid.uuid4())
        tool_data = {
            'tool_id': tool_id,
            'tool_name': tool_name,
            'tool_description': tool_description,
            'code': code,
            'version': '1.0',
        }
        self.db.save_tool(tool_data)
        self.tools.append(tool_id)
        self.persist_agent()
        self.logger.info(f"New tool created: {tool_name} (ID: {tool_id})")
        return tool_id

    def execute_tool(self, tool_id: str, *args, **kwargs):
        tool_data = self.db.get_tool(tool_id)
        if not tool_data:
            raise ValueError(f"Tool with ID {tool_id} not found")

        code = tool_data['code']
        spec = importlib.util.spec_from_loader("dynamic_tool", loader=None)
        module = importlib.util.module_from_spec(spec)
        exec(code, module.__dict__)
        sys.modules["dynamic_tool"] = module

        try:
            result = module.main(*args, **kwargs)
            self.logger.info(f"Tool {tool_id} executed successfully")
            return result
        except Exception as e:
            self.logger.error(f"Error executing tool {tool_id}: {str(e)}")
            raise

    def find_or_create_tool(self, tool_name: str, tool_description: str, code: str):
        existing_tool = self.db.find_tool_by_name(tool_name)
        if existing_tool:
            return existing_tool['tool_id']
        return self.create_tool(tool_name, tool_description, code)
    
    def communicate(self, message: str, recipient_agent_id: str) -> None:
        self.messaging_client.send_message(recipient_agent_id, message)
        self.logger.debug(f"Message sent to {recipient_agent_id}: {message}")

    def receive_message(self, message: str) -> None:
        self.logger.debug(f"Message received: {message}")
        # Process received message
        pass

    def create_sub_agent(self, agent_name, system_message, model_name, tools=None):
        sub_agent = SpecializedAgent(agent_name, system_message, model_name, tools)
        self.logger.debug(f"Sub-agent created: {sub_agent.agent_id}")
        return sub_agent

    def save_to_memory(self, key, value):
        self.memory[key] = value
        self.db.update_agent_memory(self.agent_id, self.memory)
        self.logger.debug(f"Memory updated for {self.agent_id}: {key} = {value}")
        
    def load_knowledge(self) -> Dict[str, Any]:
        knowledge = {}
        knowledge_dir = "/app/knowledge"
        for root, _, files in os.walk(knowledge_dir):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, knowledge_dir)
                knowledge[relative_path] = self.read_file(file_path)
        return knowledge

    def read_file(self, file_path: str) -> Any:
        file_extension = os.path.splitext(file_path)[1].lower()
    
        try:
            if file_extension in ['.txt', '.md', '.log']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            
            elif file_extension == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_extension == '.csv':
                return pd.read_csv(file_path).to_dict(orient='records')
            
            elif file_extension in ['.xlsx', '.xls']:
                return pd.read_excel(file_path).to_dict(orient='records')
            
            elif file_extension == '.pdf':
                with open(file_path, 'rb') as f:
                    reader = PdfReader(f)
                    return ' '.join(page.extract_text() for page in reader.pages)
            
            elif file_extension in ['.yaml', '.yml']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            
            else:
                self.logger.warning(f"Unsupported file type: {file_extension}")
                return f"Unsupported file type: {file_extension}"
        
        except Exception as e:
            self.logger.error(f"Error reading file {file_path}: {str(e)}")
            return f"Error reading file: {str(e)}"
        
    def report_status(self, task_id: str, status: str) -> None:
        """
        Reports task status to the TaskScheduler agent or logs it appropriately.
        """
        message = f"Task status for {task_id}: {status}"
        if self.config.get('task_scheduler_agent_id'):
            self.communicate(message, self.config['task_scheduler_agent_id'])
        self.logger.debug(f"Status reported: {message}")

    def report_completion(self, task_id: str, result: Any) -> None:
        """
        Reports completion to the TaskScheduler agent or logs it appropriately.
        """
        message = f"Task {task_id} completed with result: {result}"
        if self.config.get('task_scheduler_agent_id'):
            self.communicate(message, self.config['task_scheduler_agent_id'])
        self.logger.info(message)

    def report_failure(self, task_id: str, error: str) -> None:
        """
        Reports failure to the TaskScheduler agent or logs it appropriately.
        """
        message = f"Task {task_id} failed with error: {error}"
        if self.config.get('task_scheduler_agent_id'):
            self.communicate(message, self.config['task_scheduler_agent_id'])
        self.logger.error(message)          
   
    