import math
import commands2
import wpilib

from commands.flybywire import FlyByWire


class ZeroSwerveModules(commands2.CommandBase):
    def __init__(self, drivetrain, overwrite=False) -> None:
        """
        This command zeroes the swerve drive modules.
        """
        super().__init__()

        self.drivetrain = drivetrain
        self.overwrite = overwrite

        # Require full control of the drivetrain
        if not overwrite:
            self.addRequirements([self.drivetrain])

        # Timer
        self.backgroundTimer = wpilib.Timer()
        self.backgroundTimer.start()

    def initialize(self) -> None:
        self.backgroundTimer.reset()

        if self.overwrite:
            self.drivetrain.clear_swerve_zero()

    def execute(self) -> None:
        self.drivetrain.zero_swerve_modules()

    def isFinished(self) -> bool:
        return self.drivetrain.all_zeroed() or self.backgroundTimer.hasElapsed(2)

    def end(self, interrupted: bool) -> None:
        if interrupted:
            print("Swerve Zeroing was interrupted")
