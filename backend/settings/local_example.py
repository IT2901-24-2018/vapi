# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'orm',
        'HOST': 'localhost',
        'PORT': '',
        # Replace with your own settings
        'USER': 'user',
        'PASSWORD': 'password',
    }
}
