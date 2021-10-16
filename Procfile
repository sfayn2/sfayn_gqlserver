release: python manage.py migrate --no-input
release: python manage.py createsuperuser --no-input
web: gunicorn sfayn_gqlserver.wsgi
