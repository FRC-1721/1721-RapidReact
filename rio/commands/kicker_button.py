import typing
import commands2
from subsystems.yoke import kicker


class TestButtonAction(commands2.CommandBase):
    """
    System to let us tie some arbitrary action to a button for testing purposes
    """

    def __init__(self, yoke: kicker) -> None:
        super().__init__()

        self.kicker = kicker

    def initialize(self) -> None:
        self.kicker.kick()

    def isFinished(self) -> bool:
        return True
