import typing
import commands2
from wpilib import geometry
from subsystems.yoke import Yoke


class SloppyIntake(commands2.CommandBase):
    """
    Command that drives the shooter with just
    a simple set power output.
    """

    def __init__(self, yoke: Yoke, collecting_ball: bool) -> None:
        super().__init__()

        self.yoke = yoke  # This is a 'local' instance of yoke
        self.collecting_ball = collecting_ball

        # Requires yoke to operate
        self.addRequirements([self.yoke])

    def execute(self) -> None:

        # Set the intake speed
        if self.collecting_ball:
            self.yoke.setSpeed(1)
        elif not self.collecting_ball:
            self.yoke.setSpeed(-1)

    def isFinished(self) -> bool:

        # Turn off the intake
        self.yoke.setSpeed(0)
        return True
