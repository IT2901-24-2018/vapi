.PHONY: default, build, start, test, lint-only, lint-backend, lint-frontend, test-backend

BACKEND_SERVICE_NAME = django
BACKEND_LINT_FOLDERS = backend/api backend/data

FRONTEND_SERVICE_NAME = webpack

default: build start

build:
	docker-compose build

start:
	docker-compose up

test: lint-only test-only

lint-only: lint-backend lint-frontend
test-only: test-backend

lint-backend:
	docker-compose run --rm $(BACKEND_SERVICE_NAME) flake8 $(BACKEND_LINT_FOLDERS)
	docker-compose run --rm $(BACKEND_SERVICE_NAME) isort -c

lint-frontend:
	docker-compose run --rm $(FRONTEND_SERVICE_NAME) npm run lint

test-backend:
	docker-compose run --rm $(BACKEND_SERVICE_NAME) python manage.py test
