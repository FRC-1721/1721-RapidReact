# FRC 1721
# 2022

# TODO get only what we need to initalize motors
import wpilib

from rev import CANSparkMaxLowLevel, CANSparkMax
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
        self.climber_const = constants["climber"]

        # motor configuration
        self.portClimber = CANSparkMax(
            self.climber_const["port_climber"], CANSparkMaxLowLevel.MotorType.kBrushless
        )
        self.starboardClimber = CANSparkMax(
            self.climber_const["starboard_climber"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

        self.starboardClimber.follow(self.portClimber, True)

        self.starboardClimber.setInverted(False)
        self.portClimber.setInverted(True)

    def climb(self, speed):
        """
        The main purpose of the climber
        to climb
        """

        self.portClimber.set(speed)
        self.starboardClimber.set(speed)
