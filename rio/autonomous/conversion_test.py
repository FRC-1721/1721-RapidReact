import math
import commands2

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

        self.rotations_done = 0

    def execute(self) -> None:
        if self.rotations_done < 10:
            self.drivetrain.arcadeDrive(
                math.sin(self.angle) / 10,
                math.cos(self.angle) / 10,
                0,
            )

            if self.angle <= 360:
                self.angle = self.angle + 0.1
            else:
                self.angle = 0
                self.rotations_done = self.rotations_done + 1

        print(self.rotations_done)
