deploy:
	git pull
	bundle install
	bundle exec jekyll build
	cp -rv _site/* ../main/.
test:
	jekyll serve -H 0.0.0.0
