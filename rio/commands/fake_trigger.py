import typing
import commands2


class FakeTrigger(commands2.CommandBase):
    """
    System to let us tie some arbitrary action to a button for testing purposes
    """

    def __init__(self, joystick, command) -> None:
        super().__init__()
        self.joystick = joystick
        self.command = command
        self.command_run = False

    def execute(self) -> None:
        if bool(round(self.joystick.getRawAxis(2)) and self.command_run == False):
            self.command.initialize()
            self.command_run = True
        elif not bool(round(self.joystick.getRawAxis(2))):
            self.command.isFinished()
            self.command_run = False

    def isFinished(self) -> bool:

        if self.command_run:
            self.command.isFinished()
