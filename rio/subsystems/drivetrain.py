# FRC 1721
# 2022

from asyncio import constants
import logging
import math
import time

import wpilib

from wpilib import RobotBase
from wpimath import kinematics, geometry
from commands2 import SubsystemBase
from rev import CANSparkMax, CANSparkMaxLowLevel
from networktables import NetworkTables
from constants.constants import getConstants


class Drivetrain(SubsystemBase):
    """
    This class represents the whole drivetrain
    subsystem on the robot.
    """

    def __init__(self):
        super().__init__()

        # Get hardware constants
        constants = getConstants("robot_hardware")
        self.drive_const = constants["drivetrain"]

        # Configure networktables
        self.configureNetworkTables()

        # Create swerve drive modules
        # Fore port module
        self.fp_module = SwerveModule(
            self.drive_const["fp_module"],
            self.drive_const["pid"],
        )
        # Fore starboard module
        self.fs_module = SwerveModule(
            self.drive_const["fs_module"],
            self.drive_const["pid"],
        )
        # Aft port module
        self.ap_module = SwerveModule(
            self.drive_const["ap_module"],
            self.drive_const["pid"],
        )
        # Aft starboard module
        self.as_module = SwerveModule(
            self.drive_const["as_module"],
            self.drive_const["pid"],
        )

        # Create kinematics model
        # TODO: Flesh this out later...
        self.swerveKinematics = kinematics.SwerveDrive4Kinematics(
            self.fp_module.getTranslation(),
            self.fs_module.getTranslation(),
            self.ap_module.getTranslation(),
            self.as_module.getTranslation(),
        )

        # Swerve drive odometry (needs gyro.. at some point)
        # starting_pose = geometry.Pose2d(5.0, 13, geometry.Rotation2d())
        self.odometry = kinematics.SwerveDrive4Odometry(
            self.swerveKinematics, geometry.Rotation2d(0)
        )

    def periodic(self):
        """
        Called periodically when possible,
        ie: when other commands are not running.
        Odom/constant updates go here
        """
        # Update robot odometry using ModuleStates
        self.odometry.update(
            geometry.Rotation2d(0),  # This needs to be replaced with a gyro.
            self.fp_module.getActualHeading(),
            self.fs_module.getActualHeading(),
            self.ap_module.getActualHeading(),
            self.as_module.getActualHeading(),
        )

        # Networktables/dashboard
        self.fs_actual.setDouble(self.fs_module.getActualHeading().angle.radians())
        self.fs_target.setDouble(self.fs_module.getTargetHeading())
        self.as_actual.setDouble(self.as_module.getActualHeading().angle.radians())
        self.as_target.setDouble(self.as_module.getTargetHeading())
        self.fp_actual.setDouble(self.fp_module.getActualHeading().angle.radians())
        self.fp_target.setDouble(self.fp_module.getTargetHeading())
        self.ap_actual.setDouble(self.ap_module.getActualHeading().angle.radians())
        self.ap_target.setDouble(self.ap_module.getTargetHeading())

    def arcadeDrive(
        self, fwd, srf, rot
    ):  # TODO: Change scaler joystick values to set units
        """
        Generates a chassis speeds using the joystick commands
        im not sure if this is the best way to do it, but
        it can always be replaced!
        """

        # Set joystick values for later use
        self.fwd = fwd
        self.srf = srf
        self.rot = rot

        # Get wheel speeds and angles from Kinematics, given desired chassis speed and angle
        arcade_chassis_speeds = kinematics.ChassisSpeeds(fwd, srf, rot)
        _fp, _fs, _ap, _as = self.swerveKinematics.toSwerveModuleStates(
            arcade_chassis_speeds
        )

        # TODO: These modules should NOT be swapped! This is still a bug, see #1
        # https://github.com/FRC-1721/1721-RapidReact/issues/1
        self.fp_module.setModuleState(_fs)
        self.fs_module.setModuleState(_fp)
        self.ap_module.setModuleState(_as)
        self.as_module.setModuleState(_ap)

    def configureNetworkTables(self):
        # Get an instance of networktables
        self.nt = NetworkTables.getDefault()

        # Get the smart dashboard table
        self.sd = self.nt.getTable("SmartDashboard")

        self.swerve_table = self.sd.getSubTable("SwerveDrive")

        # Setup all of the networktable entries
        self.fs_actual = self.swerve_table.getEntry("fs_actual")
        self.fs_target = self.swerve_table.getEntry("fs_target")
        self.as_actual = self.swerve_table.getEntry("as_actual")
        self.as_target = self.swerve_table.getEntry("as_target")
        self.fp_actual = self.swerve_table.getEntry("fp_actual")
        self.fp_target = self.swerve_table.getEntry("fp_target")
        self.ap_actual = self.swerve_table.getEntry("ap_actual")
        self.ap_target = self.swerve_table.getEntry("ap_target")

    # self.ap_target = self.swerve_table.getEntry("ap_target")


class SwerveModule:
    """
    A custom class representing a single
    real swerve module.
    """

    def __init__(self, constants, pid):
        # Import constants
        self.constants = constants
        self.pid = pid

        # Setup one drive and one steer motor each.
        self.drive_motor = CANSparkMax(
            self.constants["drive_id"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )
        self.steer_motor = CANSparkMax(
            self.constants["steer_id"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

        # Construct the pose of this module
        self.module_pose = geometry.Translation2d(
            self.constants["pose_x"],
            self.constants["pose_y"],
        )

        # Reset both motor controllers to factory defaults
        self.drive_motor.restoreFactoryDefaults()
        self.steer_motor.restoreFactoryDefaults()

        # Construct the PID controllers
        self.steer_PID = self.steer_motor.getPIDController()

        # Assign PID Values
        self.steer_PID.setD(self.pid["steer"]["kd"])
        self.steer_PID.setI(self.pid["steer"]["ki"])
        self.steer_PID.setP(self.pid["steer"]["kp"])
        # self.steer_PID.setFF(1)
        self.steer_PID.setIMaxAccum(self.pid["steer"]["maxi"])
        self.steer_PID.setOutputRange(
            self.pid["steer"]["min_power"],
            self.pid["steer"]["max_power"],
        )

        # Assign ratios
        # self.steer_motor_encoder.setPositionConversionFactor()

        # Save all settings to flash
        # TODO: Is it a good idea to do this **every** reboot?
        self.drive_motor.burnFlash()
        self.steer_motor.burnFlash()

        # Other sensors
        self.steer_motor_encoder = self.steer_motor.getEncoder()

        # Current state variables
        self.is_zeroed = False
        self.targetState = kinematics.SwerveModuleState(
            0, geometry.Rotation2d(0)
        )  # This module state is default 0 speed, and 0 rotation

        # Simulated wheel position, only used if running the robot sim
        self.sim_encoder_pos = 0

    def getTranslation(self):
        return self.module_pose

    def setModuleState(self, newState):
        """
        Important method that updates
        the "state" (steering and speed)
        of a module.
        """
        # TODO: Use optimization at some point

        # Get the optimized (reduces unneeded movement) swerve movement from the current
        # position of the swerve module and the desired position of the swerve module
        optimizedState = kinematics.SwerveModuleState.optimize(
            newState, self.getActualHeading().angle
        )

        # debug
        if optimizedState.angle.radians() != newState.angle.radians():
            # print("Optimized!")
            pass

        # Get the desired position (in neo rotations) given by the optimized module state
        currentRef = (optimizedState.angle.radians() / (2 * math.pi)) * self.pid[
            "steer"
        ]["ratio"]

        # Set the position of the neo to the desired position
        # self.steer_motor.set(0.5)
        self.steer_PID.setReference(
            currentRef, CANSparkMaxLowLevel.ControlType.kPosition
        )

        self.targetState = newState

    def updateSimEncoder(self):
        """
        Updates the position of the simulated encoder,
        this function should be run periodicly for
        the simulated encoder to function
        """

        target = self.getTargetHeading()
        sim_fp_encoder = 0

        id = self.steer_motor.getDeviceId()  # Id's: 1,4,6,8

        # TODO: This is a bad way of doing this

        # if the current steer motor is the fp motor
        if id == self.constants["steer_id"]:

            # start a clock
            self.this_time_check = time.perf_counter()

            # try statement because one of the variables used wont exist until after this code
            try:

                # If it has been at least 0.1 secconds since the last update, update the sim encoder
                if self.this_time_check - self.last_time_check >= 0.1:

                    # if the sim encodder is less than the target, increase it at 0.3 of max speed (no PID at all)
                    if sim_fp_encoder < target:
                        sim_fp_encoder = sim_fp_encoder + (8.3 * 0.05)

                    # if the sim encodder is greater than the target, increase it at 0.3 of max speed (no PID at all)
                    else:
                        sim_fp_encoder = sim_fp_encoder - (8.3 * 0.05)
                    self.last_time_check = self.this_time_check
            except:
                self.last_time_check = self.this_time_check
            # Stopwatch check

        # Get the speed that the neo would be set to ouside of the sim
        print(sim_fp_encoder)
        return sim_fp_encoder

    def getActualHeading(self):
        """
        Returns the current module state,
        useful for odom.

        If USING_SIM is true then encoders
        are faked with simulated values
        (Not very accurate)
        """

        if not RobotBase.isReal():

            # Collect the simulated encoder position
            sim_encoder_pos = self.updateSimEncoder()

            # Divide encoder by ratio of encoder rotations to wheel rotations, times 2pi
            radians = (sim_encoder_pos / self.pid["steer"]["ratio"]) * (math.pi * 2)

            # Construct a rotation2d object
            rot = geometry.Rotation2d(radians)

            # The current state is constructed
            # TODO: Measure speed
            current_state = kinematics.SwerveModuleState(0, rot)

            return current_state

        else:
            # Current position of the motor encoder (in rotations)
            encoder = self.steer_motor_encoder.getPosition()

            # Divide encoder by ratio of encoder rotations to wheel rotations, times 2pi
            radians = (encoder / self.pid["steer"]["ratio"]) * (math.pi * 2)

            # Construct a rotation2d object
            rot = geometry.Rotation2d(radians)

            # The current state is constructed
            # TODO: Measure speed
            current_state = kinematics.SwerveModuleState(0, rot)

            # Return
            return current_state

    def getTargetHeading(self):
        """
        Returns the current heading of
        this module.
        """

        return self.targetState.angle.radians()
