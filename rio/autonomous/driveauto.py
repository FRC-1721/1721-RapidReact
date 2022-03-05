import math
import commands2
import wpilib

from commands.flywithwires import FlyWithWires
from subsystems.drivetrain import Drivetrain


class DriveAuto(commands2.SequentialCommandGroup):
    def __init__(self, drivetrain: Drivetrain) -> None:
        """
        AHH
        """
        super().__init__(
            FlyWithWires(drivetrain, fwd=-0.2, time=2),
        )
