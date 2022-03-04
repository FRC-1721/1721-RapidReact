import commands2

from subsystems.drivetrain import Drivetrain


class FlyWithWires(commands2.CommandBase):
    """
    Fires a ball at a fixed angle with no checks or fancy stuff.
    """

    def __init__(self, drivetrain: Drivetrain) -> None:
        super().__init__()

        # Local instance of drivetrain
        self.drivetrain = drivetrain

    def initialize(self) -> None:
        self.drivetrain.arcadeDrive(-0.1, 0, 0)
        print("Wires")

    def end(self, interrupted: bool) -> None:
        self.drivetrain.arcadeDrive(0, 0, 0)

        print("Fly with wires done")
