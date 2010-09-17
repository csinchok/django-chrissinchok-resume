DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = '/tmp/django-chrissinchok-resume.db'
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'chrissinchok_resume',
    'mptt',
    'dajax']
ROOT_URLCONF = 'chrissinchok_resume.urls'