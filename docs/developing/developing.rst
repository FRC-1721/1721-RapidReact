Developing
##########

Configuration
=============

.. warning::
   Make sure this manual's revision hash and the robot hash match!

This is literally the robot hardware configuration.

Use this to confirm/reconfigure motor controller addresses or examine
if pose x/y cords match actual.

.. literalinclude:: ../../rio/constants/robot_hardware.yaml
  :language: YAML


Editing and Making Docs
========================

you will need

.. code-block:: shell
   
   # Ubuntu.Debian users
   sudo apt install texlive-latex-recommended texlive-latex-extra texlive-pictures pandoc rename latexmk

Making Docs
-----------

Go into the ``Docs`` in ``pre2022season``, once there you can run

.. code-block:: shell

   pipenv install # this step may take a while
   pipenv shell
   make latexpdf # this makes a pdf of the manuel

Seeing pdfs
-----------

You should then open ``rio`` within your file manager, within ``rio`` there will be a ``_build`` in there is the pdf you just made.

Robot Simulator
===============


Requirements
------------

Go to directory ``rio`` then run

.. code-block:: shell

   pipenv install # this step may take some time
   pipenv shell
   make sim # this run the command python3 robot.py sim

This will make a simulation of the robot

Using the Simulator
-------------------

To be able to "operate" the robot while any mode will work it is recommended that under robot state, Teleoperated is enabled.
Under the Joysticks there will be Joysticks 1-5 all grayed out to select one go to System Joysticks and drag on over.
When starting up the program there will be no input method selected, under System Joysticks there may be Joysticks, Xbox controllers, or Keyboards 0-3.
Joysticks and Xbox controllers work as if piloting an actual robot.
Keyboard 0 is the WASD keys to move and E and R to rotate the controller.
Keyboards 1-3 are differing controller schemes that are useless for the purposes of testing.
