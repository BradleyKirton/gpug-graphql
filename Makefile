run: redis django tasks

redis:
	@redis-server;

tasks:
	@poetry run ./manage.py rundramatiq;

django:
	@poetry run ./manage.py runserver;

install:
	@poetry install

