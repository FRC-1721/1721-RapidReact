import typing
import commands2

from subsystems.climber import Climber
from subsystems.drivetrain import Drivetrain


class Climb(commands2.CommandBase):
    def __init__(
        self,
        climber: Climber,
        climbSpeed: typing.Callable[[], float],
    ) -> None:
        super().__init__()

        # Local instances
        self.climber = climber

        self.climbSpeed = climbSpeed

        self.addRequirements(self.climber)

    def execute(self) -> None:
        """
        Operates the climber in 'climb mode'
        """
        self.climber.climb(self.climbSpeed())

    def end(self, inturrupted):
        self.climber.climb(0)
