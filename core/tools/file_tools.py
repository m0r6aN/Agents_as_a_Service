# Tools are utility functions that can be used by multiple agents or actions. 
# They provide common functionality that isn't specific to any single agent.

import os
import hashlib

def get_file_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        buf = file.read()
        hasher.update(buf)
    return hasher.hexdigest()

def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
