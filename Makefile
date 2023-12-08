setup:
	npm install
	npm ci
build: setup
	npm run build
deploy: build
	cp -rv build/* /var/www/xhecdev/.
test: build
	npx docusaurus start
update:
	npm i @docusaurus/core@latest @docusaurus/preset-classic@latest @docusaurus/theme-mermaid@latest @docusaurus/module-type-aliases@latest