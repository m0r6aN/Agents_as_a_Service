# core/prompts/specialized_prompts.py

from .base_prompts import FILE_ANALYSIS_PROMPT

CSV_ANALYSIS_PROMPT = FILE_ANALYSIS_PROMPT + """
For CSV files, include the following information:
1. Number of rows and columns
2. Column headers
3. Data types of each column
4. Any missing or inconsistent data
"""