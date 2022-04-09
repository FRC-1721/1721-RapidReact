import commands2
import wpilib

# command imports
from autonomous.flywithwires import FlyWithWires
from commands.catapult import Catapult

# subsystems imports
from subsystems.drivetrain import Drivetrain


class DriveAuto(commands2.SequentialCommandGroup):
    def __init__(self, drivetrain: Drivetrain):
        """
        Drives in auto
        """
        super().__init__(
            # FlyWithWires(drivetrain, fwd=-0.05, time=0.75),
            FlyWithWires(drivetrain, fwd=0.05, time=0.75),
        )
