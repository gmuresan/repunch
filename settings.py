import os

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('George Muresan', 'gmuresan@umich.edu'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'repunch2_stage',                      # Or path to database file if using sqlite3.
        'USER': 'repunch2_stage',                      # Not used with sqlite3.
        'PASSWORD': 'repunchUM808',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Detroit'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1


# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = 'media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'http://repunch.s3-website-us-east-1.amazonaws.com/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = 'http://repunch.s3-website-us-east-1.amazonaws.com/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = 'http://repunch.s3-website-us-east-1.amazonaws.com/'

STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'static'),
)

# Django-storages related settings
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = 'AKIAJU3FUG5BLGG2NYPQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'repunch'
AWS_HEADERS = {
    'Cache-Control': 'max-age=86400',
}
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
CUSTOM_DOMAIN = 'http://repunch.s3-website-us-east-1.amazonaws.com/'


# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '@@(7ban@)33%@l(t=n&cpc)lb9)=h&21g_!i%r3g@_np60ah8b'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',
    'utility.facebook_functions.fb_context_processor',

)

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.gis',
    'south',
    #'imagekit',
    #'pagination',
    #'form_utils',
    #'dirtyfields',
    #'sorl.thumbnail',
    #'dajax',
    #'dajaxice',
    'boto',
    'storages',
    #'debug_toolbar',

    'account',
    'location',
    'punchcode',
    'retailer',
    'mobile',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

AUTH_PROFILE_MODULE = 'account.UserAccount'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login'

MOBILE_ENCRYPTION_KEY = 'mvbiqi289nv'

AUTHENTICATION_BACKENDS = (
    'auth.CustomerModelBackend',
    'utility.facebook_functions.FacebookAuthenticationBackend',
)

FACEBOOK_APP_ID = '141104589345410'
FACEBOOK_APP_SECRET = '6fca200d5db7652e06421006c5256e64'

EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'repunch2'
EMAIL_USE_TLS = True
EMAIL_PORT = 25
EMAIL_HOST_PASSWORD = 'repunchUM909'
DEFAULT_FROM_EMAIL = 'info@stage.repunch.com'
SERVER_EMAIL = 'info@stage.repunch.com'

try:
    from settings_local import *
except ImportError:
    pass


