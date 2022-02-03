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
Under the Joysticks there will be Joysticks 1-5 all grayed out to select one go to System Joysticks and drag on over.
When starting up the program there will be no input method selected, under System Joysticks there may be Joysticks, Xbox controllers, or Keyboards 0-3.
Joysticks and Xbox controllers work as if piloting an actual robot.
Keyboard 0 is the WASD keys to move and E and R to rotate the controller.
Keyboards 1-3 are differing controller schemes that are useless for the purposes of testing.
