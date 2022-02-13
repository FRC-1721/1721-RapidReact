import typing
import commands2
from subsystems.drivetrain import Drivetrain


class TestButtonAction(commands2.CommandBase):
    """
    System to let us tie some arbitrary action to a button for testing purposes
    """

    def __init__(self, drivetrain: Drivetrain) -> None:
        super().__init__()

        self.drivetrain = drivetrain  # This is a 'local' instance of drivetrain

    def initialize(self) -> None:
        self.drivetrain.doTestAction()

    def isFinished(self) -> bool:
        return True
