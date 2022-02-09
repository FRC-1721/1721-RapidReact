# FRC 1721
# 2022

import logging

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
        self.constants = getConstants("robot_hardware")

        # Configure networktables
        self.configureNetworkTables()

        # Create swerve drive modules
        # Fore port module
        self.fp_module = SwerveModule(self.constants["drivetrain"]["fp_module"])
        # Fore starboard module
        self.fs_module = SwerveModule(self.constants["drivetrain"]["fs_module"])
        # Aft port module
        self.ap_module = SwerveModule(self.constants["drivetrain"]["ap_module"])
        # Aft starboard module
        self.as_module = SwerveModule(self.constants["drivetrain"]["as_module"])

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
            self.fp_module.getModuleState(),
            self.fs_module.getModuleState(),
            self.ap_module.getModuleState(),
            self.as_module.getModuleState(),
        )

        # Networktables/dashboard
        self.fs_actual.setDouble(self.fs_module.getHeading())
        # self.fs_target.setDouble(self.fs_module.getHeading())
        self.as_actual.setDouble(self.as_module.getHeading())
        # self.as_target.setDouble(self.as_module.getHeading())
        self.fp_actual.setDouble(self.fp_module.getHeading())
        # self.fp_target.setDouble(self.fp_module.getHeading())
        self.ap_actual.setDouble(self.ap_module.getHeading())
        # self.ap_target.setDouble(self.ap_module.getHeading())

    def arcadeDrive(self, fwd, srf, rot):
        """
        Generates a chassis speeds using the joystick commands
        im not sure if this is the best way to do it, but
        it can always be replaced!
        """

        arcade_chassis_speeds = kinematics.ChassisSpeeds(fwd, srf, rot)
        _fp, _fs, _ap, _as = self.swerveKinematics.toSwerveModuleStates(
            arcade_chassis_speeds
        )

        # TODO: These modules should NOT be swapped! This is still a bug, see #9
        # https://github.com/FRC-1721/pre2022season/issues/9
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
        # self.fs_target = self.swerve_table.getEntry("fs_target")
        self.as_actual = self.swerve_table.getEntry("as_actual")
        # self.as_target = self.swerve_table.getEntry("as_target")
        self.fp_actual = self.swerve_table.getEntry("fp_actual")
        # self.fp_target = self.swerve_table.getEntry("fp_target")
        self.ap_actual = self.swerve_table.getEntry("ap_actual")

    # self.ap_target = self.swerve_table.getEntry("ap_target")


class SwerveModule:
    """
    Normally we inherit 'components'
    from vendors. Ex: CANSparkMax, Pneumatics,
    etc. But i think this may make it easier
    to organize.
    """

    def __init__(self, constants):
        # Setup one drive and one steer motor each.
        self.drive_motor = CANSparkMax(
            constants["drive_id"], CANSparkMaxLowLevel.MotorType.kBrushless
        )
        self.steer_motor = CANSparkMax(
            constants["steer_id"], CANSparkMaxLowLevel.MotorType.kBrushless
        )

        # Construct the pose of this module
        self.module_pose = geometry.Translation2d(
            constants["pose_x"], constants["pose_y"]
        )

        # Reset both motor controllers to factory defaults
        self.drive_motor.restoreFactoryDefaults()
        self.steer_motor.restoreFactoryDefaults()

        # Construct the PID controllers
        self.steer_PID = self.steer_motor.getPIDController()

        # Assign PID Values
        self.steer_PID.setD(0.01)
        self.steer_PID.setI(0.0001)
        self.steer_PID.setP(0.1)
        self.steer_PID.setFF(1)
        self.steer_PID.setIMaxAccum(1)
        self.steer_PID.setOutputRange(-0.5, 0.5)

        # Save all settings to flash
        self.drive_motor.burnFlash()
        self.steer_motor.burnFlash()

        # Other sensors
        self.steer_motor_encoder = self.steer_motor.getEncoder()

        # Current state variables
        self.is_zeroed = False
        self.state = kinematics.SwerveModuleState(
            0, geometry.Rotation2d(0)
        )  # This module state is default 0 speed, and 0 rotation

    def getTranslation(self):
        return self.module_pose

    def setModuleState(self, newState):
        """
        Important method that updates
        the "state" (steering and speed)
        of a module.
        """
        # self.steer_motor.set(0.5)
        self.steer_PID.setReference(
            newState.angle.radians(), CANSparkMaxLowLevel.ControlType.kPosition
        )

        print(newState.angle.radians(), self.steer_motor_encoder.getPosition())

        # TODO: Use optimization at some point
        self.state = newState

    def getModuleState(self):
        """
        Returns the current module state,
        useful for odom.
        """
        return self.state

    def getHeading(self):
        """
        Returns the current heading of
        this module
        """

        return self.state.angle.radians()
