import logging.config

# Define the logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'api_formatter': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'logstash': {
            'class': 'logstash.TCPLogstashHandler',
            'host': 'localhost',   # Replace with your Logstash host
            'port': 5044,          # Port configured in Logstash
            'version': 1,          # Logstash message format version
            'message_type': 'api', # Message type for filtering
            'fqdn': False,
            'tags': ['api'],       # Tags for identifying messages
        },
    },
    'loggers': {
        'api_logger': {
            'handlers': ['logstash'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Apply the logging configuration
logging.config.dictConfig(LOGGING_CONFIG)
