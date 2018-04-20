.PHONY: default build start stop restart migrate makemigrations shell status \
        down segment test lint-only test-only lint-backend lint-frontend test-backend

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

makemigrations:
	docker-compose run --rm $(BACKEND_SERVICE_NAME) python manage.py makemigrations

shell:
	docker-compose run --rm $(BACKEND_SERVICE_NAME) python manage.py shell

createsuperuser:
	docker-compose run --rm $(BACKEND_SERVICE_NAME) python manage.py createsuperuser

status:
	docker-compose ps

down:
	docker-compose down

# Vapi-specific
segment:
	docker-compose run --rm $(BACKEND_SERVICE_NAME) python backend/data/road_segmenting/example_roadnet_to_db.py

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
