default: upgrade-env

refresh-env-file:
	@echo 'Refreshing .env from .env.example ...'
	@cp .env.example .env

build:
	docker compose build

run:
	docker compose up --watch

run-detached:
	docker compose up -d

run-migrations: run-detached
	docker compose run processor alembic upgrade head

check-migrations:
	docker compose run processor alembic check

autogenerate-migrations: run-detached run-migrations
	docker compose run processor alembic revision --autogenerate -m $(MIGRATION_NAME);

setup-env: refresh-env-file build run-detached run-migrations

upgrade-env: build run

clean-env:
	docker compose down --volumes

reset-env: clean-env upgrade-env
