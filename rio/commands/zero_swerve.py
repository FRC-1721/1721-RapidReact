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

        self.addRequirements([self.drivetrain])

    def execute(self) -> None:
        self.drivetrain.zero_swerve_modules()

    def isFinished(self) -> bool:
        return self.drivetrain.all_zeroed()
