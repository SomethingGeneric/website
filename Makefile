ENV_FILE ?= .env.techjournals
ENV_LOADER := ./scripts/run-with-env.sh
AUTO_THEME := $(shell \
	month=$$(date +%m); \
	day=$$(date +%d); \
	if [ "$$month$$day" = "0331" ] || [ "$$month$$day" = "0401" ]; then \
		echo pain; \
	elif [ "$$month" = "10" ]; then \
		echo halloween; \
	elif [ "$$month" = "11" ] || [ "$$month" = "12" ]; then \
		echo holiday; \
	fi \
)

.PHONY: setup build dev

setup:
	@if [ ! -d node_modules ]; then \
		echo "Installing dependencies with npm ci"; \
		npm ci; \
	else \
		echo "node_modules/ already present; skipping npm ci"; \
	fi

build: setup
	@THEME="$(AUTO_THEME)"; \
	if [ -n "$$THEME" ]; then \
		echo "Using theme $$THEME"; \
		PUBLIC_DEFAULT_THEME=$$THEME $(ENV_LOADER) $(ENV_FILE) npm run build; \
	else \
		$(ENV_LOADER) $(ENV_FILE) npm run build; \
	fi

dev: setup
	@THEME="$(AUTO_THEME)"; \
	if [ -n "$$THEME" ]; then \
		echo "Using theme $$THEME"; \
		PUBLIC_DEFAULT_THEME=$$THEME $(ENV_LOADER) $(ENV_FILE) npm run dev; \
	else \
		$(ENV_LOADER) $(ENV_FILE) npm run dev; \
	fi
