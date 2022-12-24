deploy:
	git pull
	bundle install
	bundle exec jekyll build
	cp -rv _site/* /var/www/xhecdev/.
test:
	jekyll serve -H 0.0.0.0
