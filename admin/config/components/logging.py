import logging.config
import os

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'admin_formatter': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'logstash': {
            'class': 'logstash.TCPLogstashHandler',
            'host': os.environ.get('LOGSTASH_HOST', "logstash"),
            'port': 5044,
            'version': 1,
            'message_type': 'admin-app',
            'fqdn': False,
            'tags': ['admin-app'],
            'formatter': 'admin_formatter',
        },
    },
    'loggers': {
        'admin_logger': {
            'handlers': ['logstash'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
