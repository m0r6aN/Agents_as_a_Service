# tools/language_model_tool.py

from typing import Any, Dict, List
import aiohttp
import requests

class ToolParamDefinition:
    def __init__(self, param_type: str, description: str, required: bool):
        self.param_type = param_type
        self.description = description
        self.required = required

class LanguageModelTool:
    def __init__(self, name: str, model_type: str, api_endpoints: Dict[str, str], api_key: str = None, api_secret: str = None, templates: Dict[str, str] = None):
        """
        Initialize the LanguageModelTool with model details and API credentials.
        """
        self.name = name
        self.model_type = model_type
        self.api_endpoints = api_endpoints
        self.api_key = api_key
        self.api_secret = api_secret
        self.templates = templates or {}

    def generate_completion(self, prompt: str) -> str:
        """
        Generate a completion using the model's API based on the provided prompt.
        """
        endpoint = self.api_endpoints.get('completions')
        if not endpoint:
            raise ValueError("Completion endpoint is not defined for this tool.")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else None,
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            "max_tokens": 150,
        }
        
        response = self._make_api_call(endpoint, payload, headers)
        return response.get('choices')[0]['text'].strip() if response else ""

    def generate_embedding(self, input_text: str) -> List[float]:
        """
        Generate an embedding for the given input text.
        """
        endpoint = self.api_endpoints.get('embeddings')
        if not endpoint:
            raise ValueError("Embedding endpoint is not defined for this tool.")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else None,
            "Content-Type": "application/json"
        }
        
        payload = {
            "input": input_text,
        }
        
        response = self._make_api_call(endpoint, payload, headers)
        return response.get('data')[0]['embedding'] if response else []

    def summarize_text(self, input_text: str) -> str:
        """
        Summarize the given input text using the model's API.
        """
        endpoint = self.api_endpoints.get('summarize')
        if not endpoint:
            raise ValueError("Summarize endpoint is not defined for this tool.")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else None,
            "Content-Type": "application/json"
        }
        
        payload = {
            "input": input_text,
        }
        
        response = self._make_api_call(endpoint, payload, headers)
        return response.get('summary').strip() if response else ""

    def fine_tune_model(self, training_data: List[Dict[str, Any]]) -> str:
        """
        Fine-tune the model using the provided training data.
        """
        endpoint = self.api_endpoints.get('fine_tune')
        if not endpoint:
            raise ValueError("Fine-tune endpoint is not defined for this tool.")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else None,
            "Content-Type": "application/json"
        }
        
        payload = {
            "training_data": training_data,
        }
        
        response = self._make_api_call(endpoint, payload, headers)
        return response.get('fine_tune_id') if response else ""

    def _make_api_call(self, url: str, payload: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
        """
        Internal method to make API calls to the language model's endpoint.
        """
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            raise RuntimeError(f"API call failed with status code {response.status_code}: {response.text}")
        
        return response.json()
    
    async def _make_api_call_async(self, url: str, payload: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status != 200:
                    raise RuntimeError(f"API call failed with status code {response.status}: {await response.text()}")
                return await response.json()
    
    def get_params_definition(self) -> Dict[str, ToolParamDefinition]:
        return {
            "prompt": ToolParamDefinition(
                param_type="str",
                description="The prompt to send to the language model.",
                required=True,
            ),
            "max_tokens": ToolParamDefinition(
                param_type="int",
                description="The maximum number of tokens to generate.",
                required=False,
            ),
        }

    def execute(self, task_type: str, **kwargs) -> Any:
        """
        Execute a specific type of task using the language model.
        """
        if task_type == 'completion':
            return self.generate_completion(kwargs.get('prompt', ''))
        elif task_type == 'embedding':
            return self.generate_embedding(kwargs.get('input_text', ''))
        elif task_type == 'summarize':
            return self.summarize_text(kwargs.get('input_text', ''))
        elif task_type == 'fine_tune':
            return self.fine_tune_model(kwargs.get('training_data', []))
        else:
            raise ValueError(f"Task type '{task_type}' is not supported by this tool.")
