# core/system_messages/specialized_messages.py

from .base_messages import FILE_PROCESSING_MESSAGE

CSV_PROCESSING_MESSAGE = FILE_PROCESSING_MESSAGE + """
You specialize in CSV file operations. You can read CSV files, perform data analysis, and write results back to CSV format.
Always check for proper CSV formatting and handle common issues like quoting and escaping.
"""