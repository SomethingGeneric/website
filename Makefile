setup:
	npm ci
build:
	npm run build
deploy: build
	cp -rv build/* /var/www/xhecdev/.
test:
	npx docusaurus start
