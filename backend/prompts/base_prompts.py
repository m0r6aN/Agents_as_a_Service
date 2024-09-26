# core/prompts/base_prompts.py
# Prompts are templates for generating queries or instructions for agents. They can be parameterized for flexibility.

FILE_ANALYSIS_PROMPT = """
Analyze the following file:
Filename: {filename}
Size: {size} bytes
Last modified: {last_modified}

Provide a summary of the file's content and any notable characteristics.
"""