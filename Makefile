run: redis django tasks

redis:
	@redis-server;

tasks:
	@pipenv run python manage.py rundramatiq;

django:
	@pipenv run python manage.py runserver;

install:
	@pipenv install django graphene_django django-dramatiq 'dramatiq[redis, watch]' djangorestframework requests
	@pipenv install --dev jupyterlab

