from .settings import *
from dotenv import load_dotenv

load_dotenv('.env.production')

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = False

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': os.getenv('PSQL_NAME'),
#        'USER': os.getenv('PSQL_USER'),
#        'PASSWORD': os.getenv('PSQL_PASS'),
#        'HOST': os.getenv('PSQL_HOST'),
#        'PORT': os.getenv('PSQL_PORT'),
#    }
#}


ALLOWED_HOSTS = ['demo.josnin.dev']
CSRF_TRUSTED_ORIGINS = ['https://demo.josnin.dev']


#CORS
CORS_ORIGIN_WHITELIST = (
    'https://sfayn2.github.io',
)

PREFIX_URL = "sfayn-gql/"
STATIC_URL = f'/{PREFIX_URL}static/'
MEDIA_URL = f'/{PREFIX_URL}media/'
CSRF_COOKIE_NAME = "csrf-sfayn-token"

