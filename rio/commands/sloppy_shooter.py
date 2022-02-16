import typing
import commands2
from wpilib import geometry
from subsystems.yoke import Yoke


class SloppyShooter(commands2.CommandBase):
    """
    Command that drives the shooter with just
    a simple set power output.
    """

    def __init__(
        self,
        yoke: Yoke,
        speed: typing.Callable[[], float],
        angle: typing.Callable[[], float],
    ) -> None:
        super().__init__()

        self.yoke = yoke  # This is a 'local' instance of yoke
        self.speed = speed  # Callable
        self.angle = angle  # Callable

        self.angle2d = geometry.Rotation2d(self.angle())

        # Requires yoke to operate
        self.addRequirements([self.yoke])

    def execute(self) -> None:
        self.yoke.setSpeed(self.speed())
        self.yoke.setAngle(self.angle2d)
