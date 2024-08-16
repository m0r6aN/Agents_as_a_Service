# core/actions/file_actions.py
# Actions are reusable functions that agents can perform. They are typically defined as standalone functions and then associated with agents.

import os

def get_file_info(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    stats = os.stat(file_path)
    return {
        "filename": os.path.basename(file_path),
        "size": stats.st_size,
        "last_modified": stats.st_mtime,
    }

def read_file_content(file_path):
    with open(file_path, 'r') as file:
        return file.read()