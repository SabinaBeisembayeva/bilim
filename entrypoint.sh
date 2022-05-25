# !/bin/bash
python manage.py migrate

python manage.py collectstatic --noinput

#python manage.py runserver 0.0.0.0:8000

#python manage.py superuser admin@localhost admin 000000 AdminAdmin4
#
#gunicorn bilim.wsgi:application --bind 0.0.0.0:8000 --preload -w 4
#
gunicorn bilim.wsgi:application --bind 0.0.0.0:8000 --reload -w 4
