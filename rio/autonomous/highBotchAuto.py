import math
import commands2
import wpilib

from commands2 import WaitCommand

from subsystems.yoke import Yoke
from subsystems.drivetrain import Drivetrain

from commands.kicker_button import Kicker
from commands.catapult import Catapult
from commands.flywithwires import FlyWithWires
from commands.zero_swerve import ZeroSwerveModules


class HighBotchAuto(commands2.SequentialCommandGroup):
    def __init__(self, yoke: Yoke, drivetrain: Drivetrain) -> None:
        """
        AHH
        """
        super().__init__(
            FlyWithWires(drivetrain, fwd=-0.2, time=2),
            ZeroSwerveModules(drivetrain, True),
            WaitCommand(2),
            Catapult(yoke, 78.5, 0.52, True),  # Shoot like dis
            WaitCommand(2),  # Wait again
            Kicker(yoke),
        )
