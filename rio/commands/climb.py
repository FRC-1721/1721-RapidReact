import typing
import commands2

from subsystems.climber import Climber
from subsystems.drivetrain import Drivetrain


class Climb(commands2.CommandBase):
    def __init__(
        self,
        climber: Climber,
        drivetrain: Drivetrain,
        climbSpeed: typing.Callable[[], float],
        approachSpeed: typing.Callable[[], float],
    ) -> None:
        super().__init__()

        # Local instances
        self.climber = climber
        self.drivetrain = drivetrain

        self.climbSpeed = climbSpeed

        self.approachSpeed = approachSpeed

        self.addRequirements(self.climber)
        self.addRequirements(self.drivetrain)

    def execute(self) -> None:
        """
        Operates the climber in 'climb mode'
        """

        # Operate the climber actions
        self.climber.climb(self.climbSpeed())

        # Operate the drivetrain
        self.drivetrain.arcadeDrive(
            self.approachSpeed, 0, 0
        )  # Only use fwd, driving forward and backward with the approach speed value.

    def end(self, inturrupted):
        self.climber.climb(0)
        self.drivetrain.arcadeDrive(0, 0, 0)
