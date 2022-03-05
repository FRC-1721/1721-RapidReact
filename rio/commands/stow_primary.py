import commands2

from wpimath.geometry import Rotation2d
from subsystems.yoke import Yoke


class StowPrimary(commands2.CommandBase):
    """
    Command that puts the primary away when not in use.
    """

    def __init__(self, yoke: Yoke) -> None:
        super().__init__()

        self.yoke = yoke

    def initialize(self) -> None:
        self.yoke.setPrimaryYokeAngle(Rotation2d.fromDegrees(90))
