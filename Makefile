.PHONY: default build start stop restart migrate migrations \
		shell superuser status psql test lint-only test-only


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

shell:
	docker-compose run --rm $(BACKEND_SERVICE_NAME) python manage.py shell

superuser:
	docker-compose run --rm $(BACKEND_SERVICE_NAME) python manage.py createsuperuser

status:
	docker-compose ps

psql:
	docker-compose exec -u postgres postgres psql


# Testing
test: lint-only test-only

lint-only:
	docker-compose run --rm $(BACKEND_SERVICE_NAME) flake8 $(BACKEND_LINT_FOLDERS)
	docker-compose run --rm $(BACKEND_SERVICE_NAME) isort -c

test-only:
	docker-compose run --rm $(BACKEND_SERVICE_NAME) py.test
