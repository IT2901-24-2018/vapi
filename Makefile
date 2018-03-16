.PHONY: default, test, lint-only, lint-backend, lint-frontend, test-backend

default:
	echo "This is where I would build, by default."

test: lint-only test-backend

lint-only: lint-backend lint-frontend

lint-backend:
	flake8 backend/api backend/data
	isort -c

lint-frontend:
	cd frontend/; npm run lint

test-backend:
	python manage.py test

