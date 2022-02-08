# FRC 1721 Tidal Force
# 2022

# Because robotpy is so easy to use, this is moreso a
# collection of shortcuts, handy for doing simple scripts
# and macros.

all: help

help:
	@echo
	@echo "Targets:"
	@echo "   sim           Shortcut for roboy.py sim."
	@echo "   clean         Shortucut for git clean -fdX"
	@echo

# Shortcut for the simulator
sim:
	python robot.py sim

# Shortcut for deploy
deploy:
	python robot.py deploy --nc 

# Ommit the --nc, this is a custom keyword~
push:
	python robot.py deploy

# Shortcut for the download command
download:
	robotpy-installer download -r robot_requirements.txt

# Shortcut for the install command, run download first!
install:
	robotpy-installer install -r robot_requirements.txt

clean:
	git clean -fdX
