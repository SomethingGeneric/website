setup:
	git submodule update --init --recursive
	npm install
	npm ci
build: setup
	npm run build
deploy: build
	cp -rv build/* /var/www/xhecdev/.
bsddeploy:
	rsync -avc build/* root@${TGT}:/var/www/html/.
test: build
	npx docusaurus start
update:
	npm i @docusaurus/core@latest @docusaurus/preset-classic@latest @docusaurus/theme-mermaid@latest @docusaurus/module-type-aliases@latest