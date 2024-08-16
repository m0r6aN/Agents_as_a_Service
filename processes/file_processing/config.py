# File: processes/file_processing/config.py
PROCESS_CONFIG = {
    "input_directory": "/path/to/input/files",
    "output_directory": "/path/to/output/files",
    "file_types": ["csv", "txt", "json"],
    "max_file_size_mb": 100,
    "processing_timeout": 300,  # seconds
    "notification_email": "admin@domain.com",
    "retry_attempts": 3,
    "agents": {
        "file_monitor": {
            "check_interval": 30  # seconds
        },
        "file_processor": {
            "chunk_size": 1000  # rows
        },
        "data_enrichment": {
            "api_key": "your_api_key_here"
        }
    }
}