# FRC 1721
# 2022

# This code is kind of a yoke - Khan

import math

from commands2 import SubsystemBase

from ctre import TalonFX, ControlMode
from networktables import NetworkTables
from rev import CANSparkMax, CANSparkMaxLowLevel
from wpilib import RobotBase
import wpilib
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

        # Configure networktables
        self.configureNetworkTables()

        # Configure all motors
        self.starShooter = CANSparkMax(
            self.yoke_const["star_shooter_id"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

        # MOVE ME
        self.starShooter.setInverted(True)

        self.portShooter = CANSparkMax(
            self.yoke_const["port_shooter_id"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

        # MOVE ME
        self.portShooter.setInverted(True)

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

        self.kickerMotor.setInverted(True)

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

        # Configure PID
        self.auxillaryPID.setP(self.pid_const["auxillary"]["kp"])
        self.auxillaryPID.setI(self.pid_const["auxillary"]["ki"])
        self.auxillaryPID.setD(self.pid_const["auxillary"]["kd"])
        self.auxillaryPID.setD(self.pid_const["auxillary"]["ff"])
        # self.auxillaryPID.setFF(1)
        self.auxillaryPID.setIMaxAccum(self.pid_const["auxillary"]["maxi"])
        self.auxillaryPID.setOutputRange(
            self.pid_const["auxillary"]["min_power"],
            self.pid_const["auxillary"]["max_power"],
        )

        # Ratios
        self.primaryYokeMotorEncoder.setPositionConversionFactor(
            self.pid_const["ratio"]
        )
        self.auxillaryYokeMotorEncoder.setPositionConversionFactor(
            self.pid_const["ratio"]
        )

        # A handy background timer
        self.backgroundTimer = wpilib.Timer()
        self.backgroundTimer.start()

    def configureNetworkTables(self):
        # Get an instance of networktables
        self.nt = NetworkTables.getDefault()

        # Get the smart dashboard table
        self.sd = self.nt.getTable("SmartDashboard")

        # Setup subtables
        self.thermal_table = self.sd.getSubTable("Thermals")
        self.pid_NT = self.sd.getSubTable("PIDS")

        # Setup all of the networktable entries
        self.primary_yoke_temp = self.thermal_table.getEntry("primary_yoke_temp")
        self.auxillary_yoke_temp = self.thermal_table.getEntry("auxillary_yoke_temp")
        self.kicker_temp = self.thermal_table.getEntry("kicker_temp")

        self.primary_yoke_kp = self.pid_NT.getEntry("primary_yoke_kp")
        self.primary_yoke_ki = self.pid_NT.getEntry("primary_yoke_ki")
        self.primary_yoke_kd = self.pid_NT.getEntry("primary_yoke_kd")
        self.primary_yoke_ff = self.pid_NT.getEntry("primary_yoke_ff")
        self.primary_yoke_max_I = self.pid_NT.getEntry("primary_yoke_max_I")
        self.primary_yoke_max = self.pid_NT.getEntry("primary_yoke_max")
        self.primary_yoke_min = self.pid_NT.getEntry("primary_yoke_min")

        self.primary_yoke_kp.setDouble(0)
        self.primary_yoke_ki.setDouble(0)
        self.primary_yoke_kd.setDouble(0)
        self.primary_yoke_ff.setDouble(0)
        self.primary_yoke_max_I.setDouble(0)
        self.primary_yoke_max.setDouble(0)
        self.primary_yoke_min.setDouble(0)

    def setSpeed(self, speed):
        """
        Method to drive, setting
        a value from 0 to 1 by hand, no speed
        control required.
        """

        self.portShooter.set(speed)
        self.starShooter.set(-speed)

    def setVelocity(self):
        """
        Method to set the shooter speed velocity
        via pid.
        """

        # TODO: These need to be inverted, DONT do this here, do this in init
        self.starPID.setReference(
            self.setVelocity(), CANSparkMaxLowLevel.ControlType.kVelocity
        )  # self.setVelocity() sets the velocity feel free, to fix it
        self.portPID.setReference(
            self.setVelocity(), CANSparkMaxLowLevel.ControlType.kVelocity
        )

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

        actual_rotations = self.primaryYokeMotorEncoder.getPosition()

        if actual_rotations > 1 / self.pid_const["ratio"]:
            actual_rotations = actual_rotations - 1 / self.pid_const["ratio"]

        # print(
        #     f"rotation target:{target_rotations}, current: {self.getPrimaryAngle()} temp:{self.primaryYokeMotor.getMotorTemperature()}"
        # )
        # TODO: MOVE ME

        if not self.primaryYokeMotor.getMotorTemperature() > 45:
            if not target_rotations > 0.05:
                # Set a new PID target
                self.primaryPID.setReference(
                    target_rotations, CANSparkMaxLowLevel.ControlType.kPosition
                )
        else:
            self.primaryYokeMotor.set(0)

    def setAuxillaryYokeAngle(self, angle: geometry.Rotation2d):
        """
        Method to update the target angle
        for the aux.
        """

        # Convert rotation2d to radians
        target_radians = angle.radians()
        # Convert radians to motor rotations
        target_rotations = (target_radians / (2 * math.pi)) / self.pid_const["ratio"]

        # print(
        #     f"rotation target:{target_rotations}, current: {self.getAuxillaryAngle()} temp:{self.auxillaryYokeMotor.getMotorTemperature()}"
        # )

        # TODO: MOVE ME
        if not self.auxillaryYokeMotor.getMotorTemperature() > 45:
            if not target_rotations > 0.05:
                # Set a new PID target
                self.auxillaryPID.setReference(
                    target_rotations, CANSparkMaxLowLevel.ControlType.kPosition
                )
        else:
            self.auxillaryYokeMotor.set(0)

    def kick(self, kickspeed):
        """
        Activates the kicker, pushing the ball
        into the wheels.
        """

        self.kickerMotor.set(kickspeed)

    def periodic(self):
        """
        Called periodically when possible,
        ie: when other commands are not running.
        Odom/constant updates go here
        """

        if self.kickerMotor.getMotorTemperature() > 80:
            self.kickerMotor.set(0)
            print("Its running a little hot")

        if self.backgroundTimer.hasElapsed(1):  # Every 1s
            self.primary_yoke_temp.setDouble(
                self.primaryYokeMotor.getMotorTemperature()
            )
            self.auxillary_yoke_temp.setDouble(
                self.auxillaryYokeMotor.getMotorTemperature()
            )
            self.kicker_temp.setDouble(self.kickerMotor.getMotorTemperature())

    def isExtraBallPresent(self):
        """
        Returns whether a ball is held in the yoke
        TODO: check if a ball is in the yoke,
        probobly with a limit switch
        """

        return True
