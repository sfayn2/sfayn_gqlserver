from .settings import *
#import django_heroku
#import dj_database_url #something wrong can't download the latest

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('PSQL_NAME'),
        'USER': os.getenv('PSQL_USER'),
        'PASSWORD': os.getenv('PSQL_PASS'),
        'HOST': os.getenv('PSQL_HOST'),
        'PORT': os.getenv('PSQL_PORT'),
    }
}


#DATABASES['default'] = dj_database_url.parse(
#    os.getenv('DATABASE_URL'),
#)



ALLOWED_HOSTS = ['sfayn-backend.herokuapp.com']


#CORS
CORS_ORIGIN_WHITELIST = (
    'https://sfayn2.github.io',
)

# Activate Django-Heroku.
#django_heroku.settings(locals())

#TODO to separate this in production.py settings
#added after django_heroku clashing with each other & this will override django_heroku
#use dedicated Media Server to have a full control of images, it override config & use cdn for static & media
from .cdn.conf import * #noqa
