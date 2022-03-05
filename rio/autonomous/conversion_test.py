import math
import commands2
import wpilib

from commands.flybywire import FlyByWire


class ConversionTest(commands2.CommandBase):
    def __init__(self, drivetrain) -> None:
        """
        Fill this out.
        """
        super().__init__()

        self.drivetrain = drivetrain
        self.angle = 0

        self.addRequirements([self.drivetrain])

        self.backgroundTimer = wpilib.Timer()
        self.backgroundTimer.start()

    def execute(self) -> None:
        # if self.rotations_done < 10:
        #     self.drivetrain.arcadeDrive(
        #         math.sin(self.angle) / 10,
        #         math.cos(self.angle) / 10,
        #         0,
        #     )

        #     if self.angle <= 2 * math.pi:
        #         self.angle = self.angle + 0.1
        #     else:
        #         self.angle = 0
        #         self.rotations_done = self.rotations_done + 1

        # print(self.rotations_done)

        if self.backgroundTimer.hasElapsed(8):
            self.backgroundTimer.reset()
        elif self.backgroundTimer.hasElapsed(6):
            self.drivetrain.arcadeDrive(
                0,
                0,
                1,
            )
        elif self.backgroundTimer.hasElapsed(4):
            self.drivetrain.arcadeDrive(
                0,
                1,
                0,
            )
        elif self.backgroundTimer.hasElapsed(2):
            self.drivetrain.arcadeDrive(
                1,
                0,
                0,
            )
        else:
            self.drivetrain.arcadeDrive(
                0,
                0,
                0,
            )
