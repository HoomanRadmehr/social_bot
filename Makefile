.PHONY: run migrate celery beat server

PYTHON=python
MANAGE=manage.py

run: migrate celery beat server

migrate:
	$(PYTHON) $(MANAGE) makemigrations
	$(PYTHON) $(MANAGE) migrate

celery:
	nohup celery -A social_bot worker --loglevel=info > logs/celery.log 2>&1 &

beat:
	nohup celery -A social_bot beat --loglevel=info > logs/beat.log 2>&1 &

server:
	$(PYTHON) $(MANAGE) runserver 0.0.0.0:8000
