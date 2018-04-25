.PHONY: default build start stop restart migrate migrations shell superuser \
        status test lint-only test-only lint-backend lint-frontend test-backend

# Variables
BACKEND_SERVICE_NAME = django
BACKEND_LINT_FOLDERS = backend/api backend/data

FRONTEND_SERVICE_NAME = webpack

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
	docker exec -it vapi_postgres_1 psql -U postgres

# Testing
test: lint-only test-only

lint-only: lint-backend lint-frontend
test-only: test-backend

lint-backend:
	docker-compose run --rm $(BACKEND_SERVICE_NAME) flake8 $(BACKEND_LINT_FOLDERS)
	docker-compose run --rm $(BACKEND_SERVICE_NAME) isort -c

lint-frontend:
	docker-compose run --rm $(FRONTEND_SERVICE_NAME) npm run lint

test-backend:
	docker-compose run --rm $(BACKEND_SERVICE_NAME) py.test
