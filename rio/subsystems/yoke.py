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
        self.starShooter = TalonFX(self.yoke_const["shooter"]["star_falcon_id"])
        self.portShooter = TalonFX(self.yoke_const["shooter"]["port_falcon_id"])

        self.primaryYokeMotor = CANSparkMax(
            self.yoke_const["shooter"]["primary_motor"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

        self.auxillaryYokeMotor = CANSparkMax(
            self.yoke_const["shooter"]["auxillary_motor"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

        self.kickerMotor = CANSparkMax(
            self.yoke_const["shooter"]["kicker_id"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

    def Drive(self, speed):
        """
        Method to drive, setting
        a value from 0 to 1 by hand, no speed
        control required.
        """

        # Send
        self.starShooter.set(ControlMode.PercentOutput, speed)
        self.portShooter.set(ControlMode.PercentOutput, -speed)

        print(speed)

    def Rotation(
        self, degs, curDegs
    ):  # raises or lowers the shooter the inputted amount of degrees
        # degs is the amount to move, curDegs is the degrees off the ground it already is
        if (
            curDegs + degs <= 100 and curDegs + degs >= 0
        ):  # stops the shooter from going underground or into itself
            self.Rotation.set(degs)  # moves the shooter
            return curDegs + degs  # returns the updated degrees
        else:
            if degs > 0:
                self.primaryYokeMotor.set(100 - curDegs)  # moves the shooter
                return 100  # returns maximum
            else:
                self.primaryYokeMotor.set(-curDegs)  # moves the shooter
                return 0  # returns minimum

    def Kicker(
        self, degs, curDegs
    ):  # raises or lowers the Kicker the inputted amount of degrees
        # degs is the amount to move, curDegs is the degrees off the ground it already is
        if (
            curDegs + curDegs <= 60 and curDegs + curDegs >= 0
        ):  # stops the Kicker from going underground or into itself
            self.Kicker.set(degs)  # moves the Kicker
            return curDegs + degs  # returns the updated degrees
        else:
            if degs > 0:
                self.Kicker.set(60 - curDegs)  # moves the Kicker
                return 60  # returns maximum
            else:
                self.Kicker.set(-curDegs)  # moves the Kicker
                return 0  # returns minimum
