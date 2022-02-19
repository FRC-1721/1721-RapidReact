# FRC 1721
# 2022

# This code is kind of a yoke - Khan

import math

from commands2 import SubsystemBase

from ctre import TalonFX, ControlMode
from rev import CANSparkMax, CANSparkMaxLowLevel
from wpilib import RobotBase
from wpimath import geometry

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

        # MOVE ME
        self.primaryYokeMotor.setInverted(True)

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
        self.primaryPID.setP(self.pid_const["primary"]["kp"])
        self.primaryPID.setI(self.pid_const["primary"]["ki"])
        self.primaryPID.setD(self.pid_const["primary"]["kd"])
        self.primaryPID.setD(self.pid_const["primary"]["ff"])
        # self.primaryPID.setFF(1)
        self.primaryPID.setIMaxAccum(self.pid_const["primary"]["maxi"])
        self.primaryPID.setOutputRange(
            self.pid_const["primary"]["min_power"],
            self.pid_const["primary"]["max_power"],
        )

        # TODO: Auxillary yoke pid here

        # Ratios
        self.primaryYokeMotorEncoder.setPositionConversionFactor(
            self.pid_const["ratio"]
        )
        self.auxillaryYokeMotorEncoder.setPositionConversionFactor(
            self.pid_const["ratio"]
        )

    def setSpeed(self, speed):
        """
        Method to drive, setting
        a value from 0 to 1 by hand, no speed
        control required.
        """

        print(speed)

        self.portShooter.set(speed)
        self.starShooter.set(-speed)

    def setVelocity(self, velocity):
        """
        Method to set the shooter speed velocity
        via pid.
        """

        # TODO: These need to be inverted, DONT do this here, do this in init
        self.starPID.setReference(velocity, CANSparkMaxLowLevel.ControlType.kVelocity)
        self.portPID.setReference(velocity, CANSparkMaxLowLevel.ControlType.kVelocity)

    def getPrimaryAngle(self):
        return self.primaryYokeMotorEncoder.getPosition()

    def getAuxillaryAngle(self):

        return self.auxillaryYokeMotorEncoder.getPosition()

    def setPrimaryYokeAngle(self, angle: geometry.Rotation2d):
        """
        Method to update the target angle
        for the primary shooter.
        """

        # Convert rotation2d to radians
        target_radians = angle.radians()
        # Convert radians to motor rotations
        target_rotations = (target_radians / (2 * math.pi)) / self.pid_const["ratio"]

        print(
            f"rotation target:{target_rotations}, current: {self.getAuxillaryAngle()} temp:{self.primaryYokeMotor.getMotorTemperature()}"
        )

        # Set a new PID target
        self.primaryPID.setReference(
            target_rotations, CANSparkMaxLowLevel.ControlType.kPosition
        )

    def kick(self, reverse: bool = False):
        """
        Activates the kicker, pushing the ball
        into the wheels.

        TODO: Should return error if shooter is not up to speed.
        """

        if not reverse:
            self.kickerMotor.set(0.6)  # Change me!
            self.kickerMotor.set(-0.6)  # Need tweking
