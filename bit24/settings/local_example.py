# Copy this file to a file called "local.py"
# Aftwards, rename USER and PASSWORD to what you set up Postgres with.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bit24',
        'HOST': 'localhost',
        'PORT': '',
        # Replace with your own settings
        'USER': 'bit24test',
        'PASSWORD': 'test',
    }
}
