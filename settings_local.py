import os

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'repunch2_test',                      # Or path to database file if using sqlite3.
        'USER': 'repunch2_test',                      # Not used with sqlite3.
        'PASSWORD': 'repunchUM808',                  # Not used with sqlite3.
        'HOST': 'repunch2.webfactional.com',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}

#DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

STATIC_ROOT = "/static/"
STATIC_URL = '/static/'






