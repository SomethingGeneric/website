PHONY: dev

setup:
	npm ci
	npm install --os=linux --cpu=x64 sharp
build: setup
	npm run build
dev:
	npm run dev
