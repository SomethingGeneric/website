PHONY: dev

setup:
	npm ci
build: setup
	npm run build
dev: setup
	npm run dev
