.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build: ## Build docker image with dev dependencies
	@docker build --build-arg ENV=development -t facegate/user-manager:develop .

run: build ## Run application
	@docker run --rm -it -p 8003:8000 --network facegate-net --name user-manager-dev facegate/user-manager:develop

migrate-upgrade: build ## Apply migrations (upgrade)
	@docker run --rm -it --network facegate-net facegate/user-manager:develop pipenv run alembic upgrade head

migrate-downgrade: build ## Apply migrations (downgrade)
	@docker run --rm -it --network facegate-net facegate/user-manager:develop pipenv run alembic downgrade -1

lint: build ## Lint the project using Flake8
	@docker run --rm -it facegate/user-manager:develop flake8
