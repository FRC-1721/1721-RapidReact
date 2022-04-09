# FRC 1721
# 2022

# This code is kind of a yoke - Khan


import math

from commands2 import SubsystemBase

from ctre import TalonFX, ControlMode
from networktables import NetworkTables
from rev import CANSparkMax, CANSparkMaxLowLevel
from wpilib import RobotBase, SmartDashboard
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
        self.pid_const = getConstants("robot_pid")["yoke"]

        # Configure networktables
        self.configureNetworkTables()

        # Configure motors
        # Configure Shooter motors
        self.starShooter = CANSparkMax(
            self.yoke_const["star_shooter_id"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

        self.portShooter = CANSparkMax(
            self.yoke_const["port_shooter_id"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

        # Configure yoke Motors
        self.primaryYokeMotor = CANSparkMax(
            self.yoke_const["primary_motor_id"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

        # Configure Kicker motor
        self.kickerMotor = CANSparkMax(
            self.yoke_const["kicker_id"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

        # Initialize motors
        self.starShooter.restoreFactoryDefaults()
        self.portShooter.restoreFactoryDefaults()
        self.primaryYokeMotor.restoreFactoryDefaults()

        # Set motor inversions
        self.starShooter.setInverted(self.yoke_const["star_shooter_invert"])
        self.portShooter.setInverted(self.yoke_const["port_shooter_invert"])
        self.primaryYokeMotor.setInverted(self.yoke_const["primary_yoke_invert"])
        # self.auxillaryYokeMotor.setInverted(self.yoke_const["aux_yoke_invert"])
        self.kickerMotor.setInverted(self.yoke_const["kicker_invert"])

        # Get PID controller objects
        self.primaryPID = self.primaryYokeMotor.getPIDController()
        # self.auxillaryPID = self.auxillaryYokeMotor.getPIDController()
        self.starPID = self.starShooter.getPIDController()
        self.portPID = self.portShooter.getPIDController()

        # Get encoders and sensors
        self.primaryYokeMotorEncoder = self.primaryYokeMotor.getEncoder()
        # self.auxillaryYokeMotorEncoder = self.auxillaryYokeMotor.getEncoder()
        self.kickerMotorEncoder = self.kickerMotor.getEncoder()

        # Configure PID
        # Primary Yoke Pid
        self.primaryPID.setP(self.pid_const["primary"]["kp"])
        self.primaryPID.setI(self.pid_const["primary"]["ki"])
        self.primaryPID.setD(self.pid_const["primary"]["kd"])
        # self.primaryPID.setFF(1)
        self.primaryPID.setIMaxAccum(self.pid_const["primary"]["maxi"])
        self.primaryPID.setOutputRange(
            self.pid_const["primary"]["min_power"],
            self.pid_const["primary"]["max_power"],
        )

        # Shooter pid
        self.starPID.setP(self.pid_const["shooter"]["kp"])
        self.portPID.setP(self.pid_const["shooter"]["kp"])
        self.starPID.setI(self.pid_const["shooter"]["ki"])
        self.portPID.setI(self.pid_const["shooter"]["ki"])
        self.starPID.setD(self.pid_const["shooter"]["kd"])
        self.portPID.setD(self.pid_const["shooter"]["kd"])
        # self.starPID.setFF(1)
        # self.portPID.setFF(1)
        self.starPID.setIMaxAccum(self.pid_const["shooter"]["maxi"])
        self.starPID.setOutputRange(
            self.pid_const["shooter"]["min_power"],
            self.pid_const["shooter"]["max_power"],
        )
        self.portPID.setIMaxAccum(self.pid_const["shooter"]["maxi"])
        self.portPID.setOutputRange(
            self.pid_const["shooter"]["min_power"],
            self.pid_const["shooter"]["max_power"],
        )

        # Ratios
        self.primaryYokeMotorEncoder.setPositionConversionFactor(
            self.pid_const["ratio"]
        )

        # A handy background timer
        self.backgroundTimer = wpilib.Timer()
        self.backgroundTimer.start()

        # TODO: See if this works, add limit switch
        self.resetYoke(0.2695240378379822)

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
        # self.auxillary_yoke_temp = self.thermal_table.getEntry("auxillary_yoke_temp")
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
        self.starShooter.set(speed)

    def setVelocity(self, newVelocity):
        """
        Method to set the shooter speed velocity
        via pid.
        """

        # Update the velocity reference
        self.starPID.setReference(
            newVelocity,
            CANSparkMaxLowLevel.ControlType.kVelocity,
        )
        self.portPID.setReference(
            newVelocity,
            CANSparkMaxLowLevel.ControlType.kVelocity,
        )

    def getPrimaryAngle(self):
        return self.primaryYokeMotorEncoder.getPosition()

    def setPrimaryYokeAngle(self, angle: geometry.Rotation2d):
        """
        Method to update the target angle
        for the primary shooter.
        """

        # Convert rotation2d to radians
        target_radians = angle.radians()

        # Convert radians to motor rotations
        target_rotations = target_radians / (2 * math.pi)

        actual_rotations = self.primaryYokeMotorEncoder.getPosition()

        print(
            f"rotation target:{target_rotations}, current: {self.getPrimaryAngle()} temp:{self.primaryYokeMotor.getMotorTemperature()}"
        )

        if not self.primaryYokeMotor.getMotorTemperature() > 80:
            if not target_rotations < -0.05:
                # Set a new PID target
                self.primaryPID.setReference(
                    target_rotations,
                    CANSparkMaxLowLevel.ControlType.kPosition,
                )
                print("Set Reference!")
            else:
                print(f"Did not set reference, target out of range {target_rotations}")
        else:
            print(f"Motor was too hot, did not set new.")
            self.primaryYokeMotor.set(0)

    def kick(self, kickspeed):
        """
        Activates the kicker, pushing the ball
        into the wheels.
        """

        self.kickerMotor.set(kickspeed)

    def resetYoke(self, angle=0):
        """
        Should be called on enabled_init,
        DELETE ME AND REPLACE ME
        WITH A REAL LIMIT SIWTCH
        """

        self.primaryYokeMotorEncoder.setPosition(angle)
        # self.auxillaryYokeMotorEncoder.setPosition(angle)

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
            # self.auxillary_yoke_temp.setDouble(
            #     self.auxillaryYokeMotor.getMotorTemperature()
            # )
            self.kicker_temp.setDouble(self.kickerMotor.getMotorTemperature())

        SmartDashboard.putNumber(
            "Yoke/Applied_Output", self.primaryYokeMotor.getAppliedOutput()
        )

    def isExtraBallPresent(self):
        """
        Returns whether a ball is held in the yoke
        TODO: check if a ball is in the yoke,
        probobly with a limit switch
        """

        return True
