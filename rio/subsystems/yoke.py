# FRC 1721
# 2022

from commands2 import SubsystemBase

from ctre import TalonFX, ControlMode
from rev import CANSparkMax, CANSparkMaxLowLevel

from constants.constants import getConstants


class Yoke(SubsystemBase):
    """
    This class represents the whole yoke
    subsystem on the robot.
    """

    def __init__(self) -> None:
        super().__init__()

        # Configure Constants
        constants = getConstants("robot_hardware")
        self.yoke_const = constants["yoke"]

        # Configure all motors
        self.star_shooter = TalonFX(self.yoke_const["shooter"]["star_falcon_id"])
        self.port_shooter = TalonFX(self.yoke_const["shooter"]["port_falcon_id"])
        self.upperdowner = CANSparkMax(
            self.yoke_const["shooter"]["upper_downer_id"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

        # this may not be the way to do it, please ckeck later
        self.kicky = CANSparkMax(
            self.yoke_const["shooter"]["kicky_id"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

    def driveSloppy(self, speed):
        """
        Method to 'drive sloppy', setting
        a value from 0 to 1 by hand, no speed
        control required.
        """

        # Send
        self.star_shooter.set(ControlMode.PercentOutput, speed)
        self.port_shooter.set(ControlMode.PercentOutput, -speed)

        print(speed)

    def raiseDropSloppy(
        self, degs, curDegs
    ):  # raises or lowers the shooter the inputted amount of degrees
        # degs is the amount to move, curDegs is the degrees off the ground it already is
        if (
            curDegs + degs <= 100 and curDegs + degs >= 0
        ):  # stops the shooter from going underground or into itself
            self.upperdowner.set(degs)  # moves the shooter
            return curDegs + degs  # returns the updated degrees
        else:
            if degs > 0:
                self.upperdowner.set(100 - curDegs)  # moves the shooter
                return 100  # returns maximum
            else:
                self.upperdowner.set(-curDegs)  # moves the shooter
                return 0  # returns minimum

    def kickyGoSloppy(
        self, degs, curDegs
    ):  # raises or lowers the kicky the inputted amount of degrees
        # degs is the amount to move, curDegs is the degrees off the ground it already is
        if (
            curDegs + curDegs <= 60 and curDegs + curDegs >= 0
        ):  # stops the kicky from going underground or into itself
            self.kicky.set(degs)  # moves the kicky
            return curDegs + degs  # returns the updated degrees
        else:
            if degs > 0:
                self.kicky.set(60 - curDegs)  # moves the kicky
                return 60  # returns maximum
            else:
                self.kicky.set(-curDegs)  # moves the kicky
                return 0  # returns minimum
