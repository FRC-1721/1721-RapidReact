# FRC 1721 Tidal Force
# 2022

# Because robotpy is so easy to use, this is moreso a
# collection of shortcuts, handy for doing simple scripts
# and macros.

all: help

help:
	@echo
	@echo "Targets:"
	@echo "   run           Shortcut for python -m pynetworktables2js."
	@echo "   clean         Shortucut for git clean -fdX"
	@echo "   build         Shortucut for npx webpack, which builds the javascript dist files"
	@echo "   build-dev     Shortucut for npx webpack --watch, which builds the javascript dist files and autorecompiles on change"
	@echo

build:
	npx webpack

build-dev:
	npx webpack --watch

run:
	cd www && python -m pynetworktables2js

clean:
	git clean -fdX
