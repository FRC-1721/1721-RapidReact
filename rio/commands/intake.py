import commands2

from wpilib.geometry import Rotation2d

from subsystems.yoke import Yoke


class Intake(commands2.CommandBase):
    """
    Simple command to intake a ball, it does no checks.
    """

    def __init__(self, yoke: Yoke) -> None:
        super().__init__()

        self.yoke = yoke

        # Requires full control of the yoke to operate
        self.addRequirements([self.yoke])

    def initialize(self) -> None:
        self.yoke.setPrimaryYokeAngle(Rotation2d.fromDegrees(0))
        self.yoke.setSpeed(-0.25)

    def end(self, interrupted: bool) -> None:
        self.yoke.setSpeed(0)
        return True
