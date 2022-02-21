import typing
import commands2
from subsystems.drivetrain import Drivetrain


class FlyByWire(commands2.CommandBase):
    """
    FlyByWire uses pure joystick inputs
    to direct the robot. Tradionally, this
    is the most direct way to command the robot."""

    def __init__(
        self,
        drivetrain: Drivetrain,
        forward: typing.Callable[[], float],
        rotation: typing.Callable[[], float],
        strafe: typing.Callable[[], float],
    ) -> None:
        super().__init__()

        self.drivetrain = drivetrain  # This is a 'local' instance of drivetrain
        self.forward = forward  # Forward command
        self.rotation = rotation  # Rotation command
        self.strafe = strafe

        # Adding drivetrain as a requirement ensures no other command will interrupt us
        self.addRequirements([self.drivetrain])

    def execute(self) -> None:
        self.drivetrain.arcadeDrive(
            self.forward(),
            self.strafe(),
            self.rotation(),
        )
