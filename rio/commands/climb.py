import commands2
from subsystems.climber import Climber


class Climb(commands2.CommandBase):
    def __init__(self) -> None:
        # fill out later
        pass

    def execute(self, climbing: bool) -> None:
        """
        This kode should work
        """
        # Set the intake speed
        if climbing:
            Climber.setSpeed(1)
        elif not climbing:
            Climber.setSpeed(-1)

    def isFinished(self):
        self.Climber.setSpeed(0)
