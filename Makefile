PHONY: dev

setup:
	npm install
	npm ci
build: setup
	npm run build
dev:
	npm run dev
