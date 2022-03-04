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
        self.yoke.kick(0.45)
        self.backgroundTimer.reset()
        print("Kicked")

    def isFinished(self) -> bool:
        if self.backgroundTimer.hasElapsed(0.05):
            self.yoke.kick(-0.06)
            print("stop kicking")

        if self.backgroundTimer.hasElapsed(1):
            self.yoke.kick(0)
            print("Done kicking")
            return True
