setup:
	yarn install --frozen-lockfil
build:
	yarn build
deploy: build
	cp -rv build/* /var/www/xhecdev/.
test:
	npx docusaurus start
