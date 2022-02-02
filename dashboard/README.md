How to simulate the webgui.

Start by opening a shell in `rio/`

```shell
pipenv install
pipenv shell
make sim
```

Then open a shell in `dashboard/` *while the simulator
is running*

```shell
pipenv install
pipenv shell
make run
```

Tada!

You may want to test the responsiveness of the dashboard, to do this
you will need to emulate a joystick/controller. On the left side of the
screen, drag `Keyboard 0` from `System Joysticks` onto the `Joystick[0]`
location, this will enable you to use `wsad` as a joystick simulator.

Make sure to set the mode from `disabled` to `teleop` too!
