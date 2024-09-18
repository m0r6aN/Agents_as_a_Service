# utils/constants.py

# General constants
DEFAULT_MODEL_NAME = 'GPT-3.5'
DEFAULT_AGENT_VERSION = '1.0'
DEFAULT_TOOL_VERSION = '1.0'
DEFAULT_RETRY_COUNT = 3
DEFAULT_TIMEOUT = 300  # in seconds

# Task Statuses
TASK_STATUS_PENDING = 'PENDING'
TASK_STATUS_IN_PROGRESS = 'IN_PROGRESS'
TASK_STATUS_PAUSED = 'PAUSED'
TASK_STATUS_COMPLETED = 'COMPLETED'
TASK_STATUS_FAILED = 'FAILED'

# Agent Roles
AGENT_ROLE_ORCHESTRATOR = 'Orchestrator'
AGENT_ROLE_SPECIALIZED = 'Specialized'
AGENT_ROLE_MONITORING = 'Monitoring'
AGENT_ROLE_NOTIFICATION = 'Notification'
AGENT_ROLE_CHAT = 'Chat'
AGENT_ROLE_SECURITY = 'Security'

# Messaging Queues
QUEUE_PROCESS_REQUESTS = 'process_requests'
QUEUE_NOTIFICATION_AGENT = 'NotificationAgent'
QUEUE_CHAT_AGENT = 'ChatAgent'
QUEUE_SECURITY_AGENT = 'SecurityAgent'

# Logging Configuration
LOGGING_FORMAT = '%(asctime)s %(levelname)s:%(name)s: %(message)s'
LOGGING_LEVEL = 'DEBUG'

# Database Configuration
DATABASE_FILE = 'aaas.db'

# Messaging Configuration
MESSAGE_BROKER_HOST = 'localhost'

# Default Tools
DEFAULT_TOOLS = [
    'online_search',
    'memory',
    'communication',
    'code_execution',
    'prompt_generation'
]

# Miscellaneous
HEARTBEAT_INTERVAL = 30  # in seconds
