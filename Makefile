deploy:
	jekyll build
	sudo cp _site/* /var/www/main/.
test:
	jekyll serve