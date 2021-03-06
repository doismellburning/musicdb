from os.path import abspath, dirname, join

def base_dir(*xs):
    return join(dirname(dirname(dirname(dirname(abspath(__file__))))), *xs)

DEBUG = True

ADMINS = ()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'musicdb',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

SITE_URL = 'http://127.0.0.1:8000'

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

MEDIA_URL = '/storage/'
MEDIA_ROOT = base_dir('storage')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
