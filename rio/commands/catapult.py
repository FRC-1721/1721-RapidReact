import commands2

from wpimath.geometry import Rotation2d

from subsystems.yoke import Yoke


class Catapult(commands2.CommandBase):
    """
    Fires a ball at a fixed angle with no checks or fancy stuff.
    """

    def __init__(self, yoke: Yoke, angle=75, power=0.36, end=False) -> None:
        super().__init__()

        # Local instance of yoke
        self.yoke = yoke

        # Local catapult values
        self.angle = angle
        self.power = power

        # For botchauto
        self.endWhenDone = end
        self.isDone = False

        # Requires full control of the yoke to operate
        self.addRequirements([self.yoke])

    def initialize(self) -> None:
        # Set the yoke angle to 75deg
        self.yoke.setPrimaryYokeAngle(Rotation2d.fromDegrees(self.angle))

        # Set the yoke speed to a fixed 'bunt' value
        print(self.power)
        self.yoke.setSpeed(self.power)

        print("Catapulting.....")
        self.isDone = True

    def end(self, interrupted: bool) -> None:
        # Set the yoke speed back to 0
        if not self.endWhenDone:
            self.yoke.setSpeed(0)

        print("Catapult command ended")

        # Return true when done
        return True

    def isFinished(self) -> bool:
        return self.endWhenDone and self.isDone
