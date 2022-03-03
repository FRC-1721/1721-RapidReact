import typing
import commands2
from wpilib import geometry
from subsystems.yoke import Yoke


class SloppyIntake(commands2.CommandBase):
    """
    Command that drives the shooter with just
    a simple set power output.
    """

    def __init__(
        self,
        yoke: Yoke,
        max_speed: float,
        max_angle: float,
        min_angle: float,
        angle: typing.Callable[[], float],
    ) -> None:
        super().__init__()

        self.yoke = yoke  # This is a 'local' instance of yoke
        self.angle = angle  # Callable
        self.max_speed = max_speed

        # For the head-lift system
        self.max_angle = max_angle
        self.min_angle = min_angle
        self.head_acceleration = 0.01
        self.last_angle = 0

        self.angle2d = geometry.Rotation2d(self.angle())

        # Requires yoke to operate
        self.addRequirements([self.yoke])

    def execute(self) -> None:

        # Head lift math
        self.last_angle = self.clamp(
            self.min_angle,
            self.last_angle + (self.head_acceleration * self.angle()),
            self.max_angle,
        )

        self.yoke.setPrimaryYokeAngle(geometry.Rotation2d(self.last_angle))

    def clamp(self, _min, x, _max):
        """
        Minor utility function
        written by joe

        TODO: MOVE ME
        """
        return max(_min, min(x, _max))

    def isFinished(self) -> bool:
        return True