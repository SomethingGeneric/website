ENV_FILE ?= .env.techjournals
ENV_LOADER := ./scripts/run-with-env.sh

.PHONY: setup build dev

setup:
	@if [ ! -d node_modules ]; then \
		echo "Installing dependencies with npm ci"; \
		npm ci; \
	else \
		echo "node_modules/ already present; skipping npm ci"; \
	fi

build: setup
	@$(ENV_LOADER) $(ENV_FILE) npm run build

dev: setup
	@$(ENV_LOADER) $(ENV_FILE) npm run dev
