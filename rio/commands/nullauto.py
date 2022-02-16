import math
import commands2

from commands.flybywire import FlyByWire


class NullAuto(commands2.CommandBase):
    def __init__(self, drivetrain) -> None:
        """
        Fill this out.
        """
        super().__init__()

        self.drivetrain = drivetrain
        self.angle = 0

        self.addRequirements([self.drivetrain])

    def execute(self) -> None:
        self.drivetrain.arcadeDrive(math.sin(self.angle), 0, math.cos(self.angle))

        if self.angle <= 360:
            self.angle = self.angle + 0.1
        else:
            self.angle = 0

        print(self.angle)
