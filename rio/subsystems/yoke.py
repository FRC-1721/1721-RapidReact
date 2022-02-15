# FRC 1721
# 2022

from commands2 import SubsystemBase

from ctre import TalonFX, ControlMode

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
