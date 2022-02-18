# FRC 1721
# 2022

# This code is kind of a yoke - Khan

from commands2 import SubsystemBase

from ctre import TalonFX, ControlMode
from rev import CANSparkMax, CANSparkMaxLowLevel

from constants.constants import getConstants
import math


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
        self.pid_const = self.yoke_const["pid"]

        # Configure all motors
        self.starShooter = CANSparkMax(
            self.yoke_const["star_shooter_id"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

        self.portShooter = CANSparkMax(
            self.yoke_const["port_shooter_id"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

        self.primaryYokeMotor = CANSparkMax(
            self.yoke_const["primary_motor_id"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

        self.auxillaryYokeMotor = CANSparkMax(
            self.yoke_const["auxillary_motor_id"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

        self.kickerMotor = CANSparkMax(
            self.yoke_const["kicker_id"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

        # Get PID controller objects
        self.primaryPID = self.primaryYokeMotor.getPIDController()
        self.auxillaryPID = self.auxillaryYokeMotor.getPIDController()
        self.starPID = self.starShooter.getPIDController()
        self.portPID = self.portShooter.getPIDController()

        # Get encoders and sensors
        self.primaryYokeMotorEncoder = self.primaryYokeMotor.getEncoder()
        self.auxillaryYokeMotorEncoder = self.auxillaryYokeMotor.getEncoder()
        self.kickerMotorEncoder = self.kickerMotor.getEncoder()

        # Configure PID

    def setSpeed(self, speed):
        """
        Method to drive, setting
        a value from 0 to 1 by hand, no speed
        control required.
        """

        # This does not work, tested Feb 18
        # self.starPID.setReference(1.0, CANSparkMaxLowLevel.ControlType.kVelocity)
        # self.portPID.setReference(1.0, CANSparkMaxLowLevel.ControlType.kVelocity)
        self.portShooter.set(speed)
        self.starShooter.set(-speed)
        print(speed)

    def getPrimAngle(self):
        self.primaryYokeMotorEncoder = self.primaryYokeMotor.getEncoder()
        return self.primaryYokeMotorEncoder

    def getAuxAngle(self):
        self.auxillaryYokeMotorEncoder = self.auxillaryYokeMotor.getEncoder()
        return self.auxillaryYokeMotorEncoder

    def getKickMoter(self):
        self.kickerMotorEncoder = self.kickerMotor.getEncoder()
        return self.kickerMotorEncoder

    def setAngle(
        self, rot2d
    ):  # raises or lowers the shooter the inputted amount of degrees
        # rot2d is what to set it to

        curRads = rot2d.radians()  # converts rottion 2d to radians

        currentRef = curRads / (2 * math.pi)  # (radians) converted to rotations

        self.primaryPID.setReference(
            currentRef, CANSparkMaxLowLevel.ControlType.kPosition
        )  # updating the pid target

    def Kicker(
        self,
        rot2d,
    ):  # raises or lowers the shooter the inputted amount of degrees
        # rot2d is what to set it to

        curRads = rot2d.radians()  # converts rottion 2d to radians

        currentRef = curRads / (2 * math.pi)  # (radians) converted to rotations

        self.kickerPID.setReference(
            currentRef, CANSparkMaxLowLevel.ControlType.kPosition
        )  # updating the pid target