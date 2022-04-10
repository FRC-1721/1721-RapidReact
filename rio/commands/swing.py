import commands2

from wpimath.geometry import Rotation2d

from subsystems.yoke import Yoke


class Swing(commands2.CommandBase):
    """
    Fires a ball at a fixed angle with no checks or fancy stuff.
    """

    def __init__(self, yoke: Yoke) -> None:
        super().__init__()

        # Local instance of yoke
        self.yoke = yoke

        # Requires full control of the yoke to operate
        self.addRequirements([self.yoke])

    def initialize(self) -> None:
        self.yoke.setPrimaryYokeAngle(Rotation2d.fromDegrees(90))

    def isFinished(self) -> bool:
        self.yoke.setPrimaryYokeAngle(Rotation2d.fromDegrees(0))
