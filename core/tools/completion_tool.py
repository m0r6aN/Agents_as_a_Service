# tools/completion_tool.py

from tools.language_model_tool import LanguageModelTool

class CompletionTool(LanguageModelTool):
    def __init__(self, name: str, api_endpoints: Dict[str, str], api_key: str, completion_template: str = None):
        super().__init__(name, "LLM", api_endpoints, api_key)
        self.completion_template = completion_template

    def generate_completion(self, prompt: str) -> str:
        """
        Override to include a custom completion template if provided.
        """
        if self.completion_template:
            prompt = self.completion_template.format(prompt=prompt)
        return super().generate_completion(prompt)
