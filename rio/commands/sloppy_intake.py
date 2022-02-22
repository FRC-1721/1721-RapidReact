import typing
import commands2
from wpilib import geometry
from subsystems.yoke import Yoke


class SloppyIntake(commands2.CommandBase):
    """
    Command that drives the shooter with just
    a simple set power output.
    """

    def __init__(self, yoke: Yoke, collect_ball: bool, expunge_ball: bool) -> None:
        super().__init__()

        self.yoke = yoke  # This is a 'local' instance of yoke
        self.collect_ball = collect_ball
        self.expunge_ball = expunge_ball

        # Requires yoke to operate
        self.addRequirements([self.yoke])

    def execute(self) -> None:

        # Set the intake speed
        if self.collect_ball:
            self.yoke.setSpeed(1)
        elif self.expunge_ball:
            self.yoke.setSpeed(-1)
        elif not self.collect_ball and not self.expunge_ball:
            self.yoke.setSpeed(0)

    def isFinished(self) -> bool:
        return True
