import math
import commands2
import wpilib

from commands2 import WaitCommand

from subsystems.yoke import Yoke
from subsystems.drivetrain import Drivetrain

from commands.kicker_button import Kicker
from commands.catapult import Catapult
from commands.flybywire import FlyByWire
from commands.zero_swerve import ZeroSwerveModules


class BotchAuto(commands2.SequentialCommandGroup):
    def __init__(self, yoke: Yoke, drivetrain: Drivetrain) -> None:
        """
        AHH
        """
        super().__init__(
            ZeroSwerveModules(drivetrain, True),
            Catapult(yoke, 75, 0.4, True),  # Shoot like dis
            WaitCommand(2),  # Wait again
            Kicker(yoke),
        )
