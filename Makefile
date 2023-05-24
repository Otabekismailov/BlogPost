help:
	django-admin --help


mig:
	python manage.py makemigrations
	python manage.py migrate


mak:
	python manage.py makemigrations

mir:
	python manage.py migrate

run:
	python manage.py runserver