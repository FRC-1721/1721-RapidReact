import typing
import commands2

from subsystems.climber import Climber


class Climb(commands2.CommandBase):
    def __init__(self, climber: Climber, speed: typing.Callable[[], float]) -> None:
        super().__init__()

        # Local instances
        self.climber = climber
        self.speed = speed

    def execute(self) -> None:
        """
        This kode should work
        """
        # Set the intake speed
        self.climber.climb(self.speed())

    def end(self, inturrupted):
        self.climber.climb(0)
