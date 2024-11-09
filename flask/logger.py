from logging import config as logging_config
from settings import settings


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'flask_formatter': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'logstash': {
            'class': 'logstash.TCPLogstashHandler',
            'host': settings.logstash_host,
            'port': 5044,
            'version': 1,
            'message_type': 'flask-app',
            'fqdn': False,
            'tags': ['flask-app'],
            'formatter': 'flask_formatter',
        },
    },
    'loggers': {
        'flask_logger': {
            'handlers': ['logstash'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

logging_config.dictConfig(LOGGING_CONFIG)
