import commands2
import wpilib

from subsystems.yoke import Yoke


class Kicker(commands2.CommandBase):
    """
    System to let us tie some arbitrary action to a button for testing purposes
    """

    def __init__(self, yoke: Yoke) -> None:
        super().__init__()

        self.yoke = yoke

        # Timer
        self.backgroundTimer = wpilib.Timer()
        self.backgroundTimer.start()

    def initialize(self) -> None:
        self.yoke.kick(0.55)
        self.backgroundTimer.reset()

    def isFinished(self) -> bool:
        if self.backgroundTimer.hasElapsed(0.05):
            self.yoke.kick(-0.06)

        if self.backgroundTimer.hasElapsed(1):
            self.yoke.kick(0)
            return True
