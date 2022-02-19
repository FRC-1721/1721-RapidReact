# FRC 1721 Tidal Force
# 2022

# Because robotpy is so easy to use, this is moreso a
# collection of shortcuts, handy for doing simple scripts
# and macros.

ROOT := $(PWD)
STAGEDIR := $(ROOT)/_staging/

all: help

help:
	@echo
	@echo "Targets:"
	@echo "   run           Shortcut for python -m pynetworktables2js."
	@echo "   clean         Shortucut for git clean -fdX"
	@echo "   build         Shortucut for npm install && npx webpack, which builds the javascript dist files"
	@echo "   build-dev     Shortucut for npm install && npx webpack --watch, which builds the javascript dist files and autorecompiles on change"
	@echo "   deploy        Use scp to deploy the new html/js files to the nuc."
	@echo

build:
	npm install && npx webpack

# note that build-dev will not exit. It is going to continue running,
# watching all files for changes and retranspiling on a change
build-dev:
	npm install && npx webpack --watch

run:
	cd www && python -m pynetworktables2js --port=5800

comp:
	cd www && python -m pynetworktables2js --robot 10.17.21.2 --port=5800

clean:
	git clean -fdX

deploy:
	mkdir -p $(STAGEDIR)www/
	cp -r www/* $(STAGEDIR)www/
	cp -r opt/* $(STAGEDIR)

	@echo "======================================================================================="
	@echo "When prompted for a password, type 'dash' and press enter."
	@echo "======================================================================================="

	# Transfer
	scp -r $(STAGEDIR)/* dash@10.17.21.11:/opt/dashboard

	# Restart
	ssh dash@10.17.21.11 "sudo -S systemctl daemon-reload"
	ssh dash@10.17.21.11 "sudo -S systemctl restart dashboard"
