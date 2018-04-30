.PHONY: default build start stop restart migrate migrations \
		static shell superuser status psql lint test

# Variables
BACKEND_SERVICE_NAME = django
BACKEND_LINT_FOLDERS = apps/api apps/data

# General usage
default: build start

build:
	docker-compose build

start:
	docker-compose up

stop:
	docker-compose stop

restart: stop start

migrate:
	docker-compose run --rm $(BACKEND_SERVICE_NAME) python manage.py migrate

migrations:
	docker-compose run --rm $(BACKEND_SERVICE_NAME) python manage.py makemigrations

static:
	docker-compose run --rm $(BACKEND_SERVICE_NAME) python manage.py collectstatic

shell:
	docker-compose run --rm $(BACKEND_SERVICE_NAME) python manage.py shell

superuser:
	docker-compose run --rm $(BACKEND_SERVICE_NAME) python manage.py createsuperuser

status:
	docker-compose ps

psql:
	docker exec -it vapi_postgres_1 psql -U postgres

# Testing
test: lint test

lint:
	docker-compose run --rm $(BACKEND_SERVICE_NAME) flake8 $(BACKEND_LINT_FOLDERS)
	docker-compose run --rm $(BACKEND_SERVICE_NAME) isort -c

test:
	docker-compose run --rm $(BACKEND_SERVICE_NAME) py.test
