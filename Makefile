PHONY: dev

setup:
	npm ci
	npm install sharp
build: setup
	npm run build
dev:
	npm run dev
