# This triggers a command using the trigger on the controler
# TODO: This naming scheme is stupid

# NOT USING ATM

import commands2
import commands2.button

from typing import Callable


class Trigger(commands2.Trigger):
    def __init__(self: commands2._impl.Trigger, isActive: Callable[[], bool]):
        super().__init__()

        self.is_active = isActive

    def whileActiveContinous(
        self: commands2._impl.Trigger,
        command: commands2._impl.Command,
        interruptible: bool = True,
    ):
        return
