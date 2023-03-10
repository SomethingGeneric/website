deploy:
	git pull
	npm run build
	cp -rv build/* /var/www/xhecdev/.
test:
	npm run serve
