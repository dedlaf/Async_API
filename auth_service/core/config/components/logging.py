import logging.config

from auth_service.core.config.components.settings import Settings

settings = Settings()

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
            'host': settings.logstash_host,
            'port': 5044,
            'version': 1,
            'message_type': 'auth-app',
            'fqdn': False,
            'tags': ['auth-app'],
            'formatter': 'api_formatter',
        },
    },
    'loggers': {
        'auth_logger': {
            'handlers': ['logstash'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
