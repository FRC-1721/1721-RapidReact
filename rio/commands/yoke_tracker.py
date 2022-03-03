import typing
from networktables import NetworkTables
import commands2
from subsystems.drivetrain import Drivetrain


class TestButtonAction(commands2.CommandBase):
    """
    System to let us tie some arbitrary action to a button for testing purposes
    """

    def __init__(self, drivetrain: Drivetrain) -> None:
        super().__init__()

        # Get an instance of networktables
        self.nt = NetworkTables.getDefault()

        # Get the smart dashboard table
        self.limelight_table = self.nt.getTable("limelight")

        # Setup all of the networktable entries
        self.target_seen = self.limelight_table.getNumber("tv")
        self.horizontal_offset - self.limelight_table.getNumber("tx")

        self.drivetrain = drivetrain  # This is a 'local' instance of drivetrain

    def execute(self) -> None:
        pass

    def isFinished(self) -> bool:
        return True
