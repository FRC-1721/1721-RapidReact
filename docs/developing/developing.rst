Developing
##########

Configuration Files
===================

.. warning::
   Make sure this manual's revision hash and the robot hash match!

This is literally the robot hardware configuration written in yaml.

These are provided as reference for use by pit crew.

Use this to confirm/reconfigure motor controller addresses or examine
if pose x/y cords match actual.

.. literalinclude:: ../../rio/constants/robot_hardware.yaml
  :language: YAML


Getting started modifying these docs
====================================

Requirements for building the docs
----------------------------------

You'll need to install several packages to build these docs

.. code-block:: shell
   
   # Ubuntu/Debian users
   sudo apt install texlive-latex-recommended texlive-latex-extra texlive-pictures pandoc rename latexmk

Making the docs
---------------

Under the ``Docs`` directory in ``pre2022season``, setup a pipenv using the 
provided files and invoke the ``make latexpdf`` command to build the docs.

.. code-block:: shell

   pipenv install # May take a while
   pipenv shell
   make latexpdf # Builds the manual

Find the generated ``.pdf`` under ``docs/_build/latex/``


Robot Simulator
===============


Requirements
------------

Under the ``rio`` directory run

.. code-block:: shell
   
   pipenv install # May take a while
   pipenv shell
   make sim # Alternatively run: python3 robot.py sim

This will start the robot simulator. See :ref:`Using the Simulator` for more info.

Using the Simulator
-------------------

To be able to "operate" the robot while any mode will work it is recommended that under robot state, Teleoperated is enabled.
Under the Joysticks there will be Joysticks 1-5 all grayed out, to select one go to System Joysticks and drag on over.
When starting up the program there will be no input method selected under System Joysticks there may be Joysticks, Xbox controllers, or Keyboards 0-3.
Joysticks and Xbox controllers work as if piloting an actual robot.
Keyboard 0 is the WASD keys to move and E and R to rotate the controller.
Keyboards 1-3 are differing controller schemes that are useless for the purposes of testing due to lack of movement.
Keyboard inputs require you to have the active window be the simulator while, Joysticks and xbox controllers don't.

Web Station
===========

Requirements
------------

under the ``dashboard`` directory run

.. code-block:: shell

   pipenv install # May take a while
   pipenv shell
   make run # makes a local hosted website dashboard

This will start the website dashboard. See :ref:`Using the Web Station` for more info.

Using the Web Station
---------------------

Activating the dashboard doesn't automaticaly start. To start the Web Station within your terminal it will print

.. code-block::

   cd www && python -m pynetworktables2js
   16:32:28:683 INFO    : dashboard           : Connecting to NetworkTables at Ip address
   16:32:28:683 INFO    : nt                  : NetworkTables initialized in client mode
   16:32:28:683 INFO    : dashboard           : NetworkTables Initialized
   16:32:28:684 INFO    : dashboard           : Listening on http://localhost:8888/
   16:32:28:978 INFO    : tornado.access      : 101 GET /networktables/ws (Ip address) 0.89ms
   16:32:28:978 INFO    : net2js              : NetworkTables websocket opened

Within this you will see one called local host, you will need to copy that link and put it in a web browser.
It is recommened that you use this in incognito due to network cache causing issues with not updating.
In the top left there will display a simulation of the swerve drive wheels.
To see the simulation of the swerve drive you first must turn the wheels.
In the top right there is an autonomous selector where autonomous may be selected.
There is also a camera that are on the bot.
