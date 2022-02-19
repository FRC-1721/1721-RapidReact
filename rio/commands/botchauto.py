import math
import commands2
import wpilib

from subsystems.yoke import Yoke
from subsystems.drivetrain import Drivetrain

from commands.kicker_button import Kicker


class BotchAuto(commands2.CommandBase):
    def __init__(self, yoke: Yoke, drivetrain: Drivetrain) -> None:
        """
        AHH
        """
        super().__init__()

        self.yoke = yoke

        self.addRequirements([self.yoke, drivetrain])

        self.backgroundTimer = wpilib.Timer()
        self.backgroundTimer.start()

    def initialize(self) -> None:
        wpilib.wait(4)
        self.yoke.setSpeed(-0.524)
        wpilib.wait(1)
        self.yoke.kick(0.4)
        self.backgroundTimer.reset()

    def isFinished(self) -> bool:
        if self.backgroundTimer.hasElapsed(0.05):
            self.yoke.kick(-0.06)

        if self.backgroundTimer.hasElapsed(1):
            self.yoke.kick(0)
            self.yoke.setSpeed(0)
            return True
