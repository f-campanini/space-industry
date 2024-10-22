from pathlib import Path
from celery.schedules import crontab
import configparser
import os

parser = configparser.ConfigParser()
parser.read("config.ini")
DEBUG = parser.get('settings', 'DEBUG')
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = parser.get('settings', 'SECRET_KEY')

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    # custom
    'scraping.apps.ScrapingConfig',
    
    # default    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_results',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'spaceindustry.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'spaceindustry.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Media files (Images)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR

# celery
CELERY_BROKER_URL = 'amqp://localhost:5672'
CELERY_RESULT_BACKEND = 'amqp://localhost:5672'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_IMPORTS = ('scraping.tasks', 'scraping.metrics', 'scraping.twitter')
CELERY_BEAT_SCHEDULE = {
    "execute_scraping": {
        "task": "scraping.tasks.run_scraper",
        "schedule": crontab(minute="*/60"),
    },
    "execute_metrics": {
        "task": "scraping.metrics.run_wordcloud",
        "schedule": crontab(minute="*/240"),
    },
    "execute_twitter_search": {
        "task": "scraping.twitter.store_tweets",
        "schedule": crontab(minute="*/2"),
    },    
}
