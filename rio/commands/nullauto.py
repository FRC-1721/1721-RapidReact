import commands2

from commands.flybywire import FlyByWire


class NullAuto(commands2.SequentialCommandGroup):
    def __init__(self, drivetrain) -> None:
        """
        Fill this out.
        """
        super().__init__()

        # list of commands.
        self.addCommands(
            FlyByWire(
                drivetrain,
                lambda: self.getNum(0),
                lambda: self.getNum(1),
                lambda: self.getNum(0),
            ),
        )

    def getNum(self, num):
        """
        Replace me later.
        Typing weirdness.
        """

        return num
