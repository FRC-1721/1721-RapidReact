import commands2
import constants

from networktables import NetworkTables

from subsystems.drivetrain import Drivetrain
from subsystems.yoke import Yoke


class vision(commands2.SequentialCommandGroup):
    """
    A vision command
    """

    def __init__(self, drive: Drivetrain, yoke: Yoke):
        super().__init__()
        NetworkTables.getTable("limelight").getNumber("<variablename>")

    def camera(self):
        pass
