import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('ADMIN_DB_NAME'),
        'USER': os.environ.get('ADMIN_DB_USER'),
        'PASSWORD': os.environ.get('ADMIN_DB_PASSWORD'),
        'HOST': os.environ.get('ADMIN_DB_HOST', 'db'),
        'PORT': os.environ.get('ADMIN_DB_PORT', 5432),
        'OPTIONS': {
            'options': '-c search_path=public,content'
        }
    }
}