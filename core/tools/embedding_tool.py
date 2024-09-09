# tools/embedding_tool.py
# EmbeddingTool Subclass:

from typing import Dict, List
from tools.language_model_tool import LanguageModelTool

class EmbeddingTool(LanguageModelTool):
    def __init__(self, name: str, api_endpoints: Dict[str, str], api_key: str):
        super().__init__(name, "SLM", api_endpoints, api_key)

    def generate_embedding(self, input_text: str) -> List[float]:
        """
        Override for additional pre-processing if needed.
        """
        # Add any special pre-processing for embedding generation here
        return super().generate_embedding(input_text)
