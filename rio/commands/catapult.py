import commands2

from wpimath.geometry import Rotation2d

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
        # Set the yoke angle to 75deg
        self.yoke.setPrimaryYokeAngle(Rotation2d.fromDegrees(75))

        # Set the yoke speed to a fixed 'bunt' value
        self.yoke.setSpeed(0.4)

        print("Catapulting.....")

    def end(self, interrupted: bool) -> None:
        # Set the yoke speed back to 0
        self.yoke.setSpeed(0)

        print("Catapult done")

        # Return true when done
        return True
