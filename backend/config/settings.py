# config/settings.py

import os

# Base Directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database Configuration
DATABASE = {
    'ENGINE': 'sqlite3',
    'NAME': os.path.join(BASE_DIR, 'database', 'aaas.db'),
}

# Messaging Configuration
MESSAGE_BROKER = {
    'HOST': 'localhost',
    'PORT': 5672,
    'VIRTUAL_HOST': '/',
    'USERNAME': 'guest',
    'PASSWORD': 'guest',
    'HEARTBEAT': 600,
    'BLOCKED_CONNECTION_TIMEOUT': 300,
}

# Logging Configuration
LOGGING_CONFIG_FILE = os.path.join(BASE_DIR, 'config', 'logging.conf')

# Agent Configuration
AGENT_DEFAULTS = {
    'MODEL_NAME': 'GPT-3.5',
    'VERSION': '1.0',
    'RETRY_COUNT': 3,
    'TIMEOUT': 300,  # seconds
    'TOOLS': [
        'online_search',
        'memory',
        'communication',
        'code_execution',
        'prompt_generation',
    ],
}

# Security Configuration
SECURITY_SETTINGS = {
    'AUTHENTICATION_ENABLED': True,
    'AUTHORIZATION_ENABLED': True,
    'ENCRYPTION_KEY': os.environ.get('ENCRYPTION_KEY', 'default_encryption_key'),
}

# Other Settings
HEARTBEAT_INTERVAL = 30  # seconds
CHECK_INTERVAL = 5       # seconds for MonitoringAgent
SCAN_INTERVAL = 60       # seconds for SecurityAgent

# Environment-Specific Settings
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')

if ENVIRONMENT == 'production':
    # Override settings for production
    MESSAGE_BROKER['USERNAME'] = os.environ.get('BROKER_USERNAME', 'prod_user')
    MESSAGE_BROKER['PASSWORD'] = os.environ.get('BROKER_PASSWORD', 'prod_pass')
    DATABASE['ENGINE'] = 'postgresql'
    DATABASE['NAME'] = os.environ.get('DATABASE_NAME', 'aaas_prod')
    DATABASE['USER'] = os.environ.get('DATABASE_USER', 'db_user')
    DATABASE['PASSWORD'] = os.environ.get('DATABASE_PASSWORD', 'db_pass')
    DATABASE['HOST'] = os.environ.get('DATABASE_HOST', 'localhost')
    DATABASE['PORT'] = os.environ.get('DATABASE_PORT', '5432')
