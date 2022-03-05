import commands2
import wpilib

from subsystems.drivetrain import Drivetrain


class FlyWithWires(commands2.CommandBase):
    """
    Fires a ball at a fixed angle with no checks or fancy stuff.
    """

    def __init__(self, drivetrain: Drivetrain, fwd=0, srf=0, rot=0, time=-1) -> None:
        super().__init__()

        # Local instance of drivetrain
        self.drivetrain = drivetrain

        self.time = time
        self.fwd = fwd
        self.srf = srf
        self.rot = rot

        self.addRequirements([drivetrain])

        # Timer
        self.backgroundTimer = wpilib.Timer()
        self.backgroundTimer.start()

    def initialize(self) -> None:
        self.backgroundTimer.reset()

    def execute(self) -> None:
        self.drivetrain.arcadeDrive(
            self.fwd,
            self.srf,
            self.rot,
        )

    def end(self, interrupted: bool) -> None:
        self.drivetrain.arcadeDrive(0, 0, 0)

        print("Fly with wires done")

    def isFinished(self) -> bool:
        if self.time != -1 and self.backgroundTimer.hasElapsed(self.time):
            return True
