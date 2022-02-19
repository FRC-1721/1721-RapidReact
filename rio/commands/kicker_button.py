import typing
import commands2
from subsystems.yoke import Yoke


class Kicker(commands2.CommandBase):
    """
    System to let us tie some arbitrary action to a button for testing purposes
    """

    def __init__(self, yoke: Yoke) -> None:
        super().__init__()

        self.yoke = yoke

    def initialize(self) -> None:
        self.yoke.kick()

    def isFinished(self) -> bool:
        return True
