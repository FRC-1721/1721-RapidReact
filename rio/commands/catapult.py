import commands2

from wpilib.geometry import Rotation2d

from subsystems.yoke import Yoke


class Catapult(commands2.CommandBase):
    """
    Fires a ball at a fixed angle with no checks or fancy stuff.
    """

    def __init__(self, yoke: Yoke) -> None:
        super().__init__()

        self.yoke = yoke

        # Requires full control of the yoke to operate
        self.addRequirements([self.yoke])

    def initialize(self) -> None:
        self.yoke.setPrimaryYokeAngle(Rotation2d.fromDegrees(75))
        self.yoke.setSpeed(0.8)

    def end(self, interrupted: bool) -> None:
        self.yoke.setSpeed(0)
        return True
