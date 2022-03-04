import commands2
import wpilib

from subsystems.drivetrain import Drivetrain


class FlyWithWires(commands2.CommandBase):
    """
    Fires a ball at a fixed angle with no checks or fancy stuff.
    """

    def __init__(self, drivetrain: Drivetrain, time=-1) -> None:
        super().__init__()

        # Local instance of drivetrain
        self.drivetrain = drivetrain

        self.time = time

        # Timer
        self.backgroundTimer = wpilib.Timer()
        self.backgroundTimer.start()

    def initialize(self) -> None:
        self.drivetrain.arcadeDrive(-0.2, 0, 0)
        print("Wires")

    def end(self, interrupted: bool) -> None:
        self.drivetrain.arcadeDrive(0, 0, 0)

        print("Fly with wires done")

    def isFinished(self) -> bool:
        if self.time != -1 and self.backgroundTimer.hasElapsed(self.time):
            return True
