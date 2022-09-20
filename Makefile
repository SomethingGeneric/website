deploy:
	git pull
	bundle exec jekyll build
	sudo cp -rv _site/ ../main
test:
	jekyll serve
