.PHONY: default build start down stop restart migrate migrations \
		static shell superuser status psql test lint-only test-only

# Variables
BACKEND_SERVICE_NAME = django
BACKEND_LINT_FOLDERS = apps/api apps/data


# General usage
default: build start

build:
	docker-compose build

start:
	docker-compose up

down:
	docker-compose down

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
	docker-compose exec -u postgres postgres psql


# Testing
test: lint-only test-only

lint-only:
	docker-compose run --rm $(BACKEND_SERVICE_NAME) flake8 $(BACKEND_LINT_FOLDERS)
	docker-compose run --rm $(BACKEND_SERVICE_NAME) isort -c

<<<<<<< HEAD
test-only:
	docker-compose run --rm $(BACKEND_SERVICE_NAME) py.test
=======
test:
	docker-compose run --rm $(BACKEND_SERVICE_NAME) py.test --cov=apps
>>>>>>> dev
