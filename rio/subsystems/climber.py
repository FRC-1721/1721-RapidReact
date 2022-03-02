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
        self.Climber_const = constants["Climber"]

        # motor configuration
        self.portClimber = CANSparkMax(1, CANSparkMaxLowLevel.MotorType.kBrushless)
        self.starboardClimber = CANSparkMax(2, CANSparkMaxLowLevel.MotorType.kBrushless)

        self.starboardClimber.follow(self.portClimber, True)

        self.backgroundTimer = wpilib.Timer()
        self.backgroundTimer.start()

        self.climbPID = self.portClimber.getPIDController()

        self.climbPID.setP("kp")
        self.climbPID.setI("ki")
        self.climbPID.setD("kd")

    def climb(self, speed):
        """
        The main purpose of the climber
        to climb
        """

        self.climbPID.setReference(speed, CANSparkMaxLowLevel.ControlType.kVelocity)
