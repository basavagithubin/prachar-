release: python manage.py migrate --noinput
web: gunicorn candidate_management.wsgi:application
