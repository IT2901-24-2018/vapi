# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'orm',
        'HOST': 'localhost',
        'PORT': '',
        # Replace with your own settings
        'USER': 'user',
        'PASSWORD': 'password',
    }
}
