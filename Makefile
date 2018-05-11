.PHONY: default build start down stop restart migrate migrations \
		superuser psql test lint-only test-only

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
	docker-compose run --rm django python manage.py migrate

migrations:
	docker-compose run --rm django python manage.py makemigrations

superuser:
	docker-compose run --rm django python manage.py createsuperuser

psql:
	docker-compose exec -u postgres postgres psql


# Testing
test: lint-only test-only

lint-only:
	docker-compose run --rm django flake8 apps/
	docker-compose run --rm django isort -c

test-only:
	docker-compose run --rm django py.test --cov-config=setup.cfg --cov=apps
