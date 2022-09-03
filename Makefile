deploy:
	git pull
	bundle exec jekyll build
	sudo cp -rv _site/* /var/www/main/.
test:
	jekyll serve