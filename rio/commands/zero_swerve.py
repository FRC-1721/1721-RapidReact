import math
import commands2
import wpilib

from commands.flybywire import FlyByWire


class ZeroSwerveModules(commands2.CommandBase):
    def __init__(self, drivetrain) -> None:
        """
        This command zeroes the swerve drive modules.
        """
        super().__init__()

        self.drivetrain = drivetrain

        # Require full control of the drivetrain
        self.addRequirements([self.drivetrain])

        # Timer
        self.backgroundTimer = wpilib.Timer()
        self.backgroundTimer.start()

    def initialize(self) -> None:
        self.backgroundTimer.reset()

    def execute(self) -> None:
        self.drivetrain.zero_swerve_modules()

    def isFinished(self) -> bool:
        return self.drivetrain.all_zeroed() or self.backgroundTimer.hasElapsed(2)
