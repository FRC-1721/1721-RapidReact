import commands2
from subsystems.climber import Climber


class climb(commands2.CommandBase):
    def __init__(self) -> None:
        # fill out later
        pass

    def upwards(self) -> None:
        """
        This kode should work
        """
        # Set the intake speed
        if self.climbing:
            self.Climber.setSpeed(1)
        elif not self.climbing:
            self.Climber.setSpeed(-1)
        else:
            self.Climber.setSpeed(0)
