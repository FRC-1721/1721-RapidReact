import typing
import commands2

from wpimath.geometry import Rotation2d

from subsystems.climber import Climber
from subsystems.yoke import Yoke


class Climb(commands2.CommandBase):
    def __init__(
        self,
        climber: Climber,
        yoke: Yoke,
        climbSpeed: typing.Callable[[], float],
    ) -> None:
        super().__init__()

        # Local instances
        self.climber = climber
        self.yoke = yoke

        self.climbSpeed = climbSpeed

        self.addRequirements(self.climber)

    def execute(self) -> None:
        """
        Operates the climber in 'climb mode'
        """

        if abs(self.climbSpeed()) > 0.1:
            self.climber.climb(self.climbSpeed())
            self.yoke.setPrimaryYokeAngle(Rotation2d.fromDegrees(85))
        else:
            self.climber.climb(0)

    def end(self, inturrupted):
        self.climber.climb(0)
