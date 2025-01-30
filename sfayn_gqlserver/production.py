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



CSRF_COOKIE_NAME = "_csrf-s"
VIEW_SITE_URL = "/sfayn-gql/graphql/"
SESSION_COOKIE_NAME = "_s-id"

