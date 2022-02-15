# FRC 1721
# 2022

# TODO get only what we need to initalize motors
import rev
from constants.constants import getConstants
from commands2 import Subsystem, SubsystemBase


class Climber(SubsystemBase):
    """
    This class represents the Climber
    as a whole
    """

    def __init__(self) -> None:
        super().__init__()

        # get Constants
        constants = getConstants("robot_hardware")
        self.Climber_const = constants["Climber"]

        # motor configuration
        self.portClimber = rev.CANSparkMax(1, rev.MotorType.kBrushless)
        self.starboardClimber = rev.CANSparkMax(2, rev.MotorType.kBrushless)

        self.motors = (self.portClimberLeader, self.starboardClimberOne)

    def climb(self, speed):
        """
        The main purpose of the climber
        to climb
        """
