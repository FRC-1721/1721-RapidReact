How to simulate the webgui.

Note that you need to have both pipenv and node.js installed. To install node.js:
- Follow the instructions to install NVM [here](https://github.com/creationix/nvm#install-script)
- Install the correct version of node (probably the current LTS version using `nvm install --lts` but check the `package.json` file in this directory for the version listed under `engines`)

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
make build
make run
```

Tada!

You may want to test the responsiveness of the dashboard, to do this
you will need to emulate a joystick/controller. On the left side of the
screen, drag `Keyboard 0` from `System Joysticks` onto the `Joystick[0]`
location, this will enable you to use `wsad` as a joystick simulator.

Make sure to set the mode from `disabled` to `teleop` too!
