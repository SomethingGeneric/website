deploy:
	git pull
	bundle exec jekyll build
	cp -rv _site/ ../main
test:
	jekyll serve
