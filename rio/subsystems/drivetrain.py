# FRC 1721
# 2022

import math


from wpilib import RobotBase

from wpimath import kinematics, geometry
from commands2 import SubsystemBase

from rev import CANSparkMax, CANSparkMaxLowLevel
from ctre import Pigeon2, Pigeon2Configuration

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

        # Setup Pigeon
        # Docs: https://docs.ctre-phoenix.com/en/stable/ch11_BringUpPigeon.html?highlight=pigeon#pigeon-api
        imuConst = constants["drivetrain"]["imu"]  # IMU constants
        self.imu = Pigeon2(imuConst["can_id"])  # Create object

        # Setup Pigeon pose
        self.imu.configMountPose(
            imuConst["yaw"],
            imuConst["pitch"],
            imuConst["roll"],
        )

        # Create kinematics model
        # TODO: Flesh this out later...
        self.swerveKinematics = kinematics.SwerveDrive4Kinematics(
            self.fp_module.getPose(),
            self.fs_module.getPose(),
            self.ap_module.getPose(),
            self.as_module.getPose(),
        )

        # Swerve drive odometry (needs gyro.. at some point)
        # starting_pose = geometry.Pose2d(5.0, 13, geometry.Rotation2d())
        self.odometry = kinematics.SwerveDrive4Odometry(
            self.swerveKinematics,
            self.getGyroHeading(),
        )

    def doTestAction(self):
        print("I am doing a test action.")
        self.fs_module.doTestAction()

    def periodic(self):
        """
        Called periodically when possible,
        ie: when other commands are not running.
        Odom/constant updates go here
        """
        # Update robot odometry using ModuleStates
        self.odometry.update(
            self.getGyroHeading(),
            self.fp_module.getCurrentState(),
            self.fs_module.getCurrentState(),
            self.ap_module.getCurrentState(),
            self.as_module.getCurrentState(),
        )

        # Networktables/dashboard
        self.fs_actual.setDouble(self.fs_module.getCurrentState().angle.radians())
        self.fs_target.setDouble(self.fs_module.getTargetHeading())
        self.as_actual.setDouble(self.as_module.getCurrentState().angle.radians())
        self.as_target.setDouble(self.as_module.getTargetHeading())
        self.fp_actual.setDouble(self.fp_module.getCurrentState().angle.radians())
        self.fp_target.setDouble(self.fp_module.getTargetHeading())
        self.ap_actual.setDouble(self.ap_module.getCurrentState().angle.radians())
        self.ap_target.setDouble(self.ap_module.getTargetHeading())

    def arcadeDrive(self, fwd, srf, rot):
        """
        Generates a chassis speeds using the joystick commands
        im not sure if this is the best way to do it, but
        it can always be replaced!
        """

        fwd_velocity = fwd * self.drive_const["max_velocity"]
        srf_velocity = srf * self.drive_const["max_velocity"]

        # Get wheel speeds and angles from Kinematics, given desired chassis speed and angle
        arcade_chassis_speeds = kinematics.ChassisSpeeds(
            fwd_velocity, srf_velocity, rot
        )

        _fp, _fs, _ap, _as = self.swerveKinematics.toSwerveModuleStates(
            arcade_chassis_speeds
        )

        if (
            max(_fp.speed, _fs.speed, _ap.speed, _as.speed)
            > self.drive_const["min_velocity"]
        ):
            # TODO: These modules should NOT be swapped! This is still a bug, see #1
            # https://github.com/FRC-1721/1721-RapidReact/issues/1
            self.fp_module.setDesiredState(_fs)
            self.fs_module.setDesiredState(_fp)
            self.ap_module.setDesiredState(_as)
            self.as_module.setDesiredState(_ap)

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

    def getGyroHeading(self):
        """
        Returns the gyro heading.
        """

        return geometry.Rotation2d.fromDegrees(self.imu.getYaw())


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
        self.drive_PID = self.drive_motor.getPIDController()

        # Assign PID Values
        # TODO: PID values currently the same for both steering and driveing
        self.steer_PID.setP(self.pid["steer"]["kp"])
        self.steer_PID.setI(self.pid["steer"]["ki"])
        self.steer_PID.setD(self.pid["steer"]["kd"])

        self.drive_PID.setP(self.pid["drive"]["kp"])
        self.drive_PID.setI(self.pid["drive"]["ki"])
        self.drive_PID.setD(self.pid["drive"]["kd"])
        self.drive_PID.setFF(self.pid["drive"]["ff"])

        # self.steer_PID.setFF(1)
        self.steer_PID.setIMaxAccum(self.pid["steer"]["maxi"])
        self.steer_PID.setOutputRange(
            self.pid["steer"]["min_power"],
            self.pid["steer"]["max_power"],
        )

        self.drive_PID.setIMaxAccum(self.pid["steer"]["maxi"])
        self.drive_PID.setOutputRange(
            self.pid["steer"]["min_power"],
            self.pid["steer"]["max_power"],
        )

        # Other sensors
        self.steer_motor_encoder = self.steer_motor.getEncoder()
        self.steer_motor_encoder.setPositionConversionFactor(self.pid["steer"]["ratio"])

        # Save all settings to flash
        # TODO: Is it a good idea to do this **every** reboot?
        # NOTES from Turner's Testing
        # If you don't run burnFlash, then setPositionConversionFactor appears to work.
        # If you run burnFlash before setPositionConversionFactor, conversion factor is not set.
        # if you run burnFlash after setPositionConversionFactor, converstion factor IS set.
        # we've decided to never burnFlash and instead leave all settings volatile.
        self.drive_motor.burnFlash()
        self.steer_motor.burnFlash()
        print(
            "Steer Drive:",
            self.constants["steer_id"],
            "Start Position: ",
            self.steer_motor_encoder.getPosition(),
        )

        # Reset the position of the encoder.
        # TODO: We need to set this position when the optical limit switch
        # triggers
        self.steer_motor_encoder.setPosition(0)

        # Current state variables
        self.isZeroed = False
        # By default: 0 speed, and 0 rotation
        self.desiredState = kinematics.SwerveModuleState(0, geometry.Rotation2d(0))

        self.angleSum = 0  # Delete me

    def doTestAction(self):
        """
        This is triggered on the A button on the xbox controller. You can use
        this to test some code on button press.

        Delete whenever not needed anymore.
        """
        res = self.steer_motor_encoder.setPosition(0)
        print(
            "Steer Drive:",
            self.constants["steer_id"],
            "Immediate Position: ",
            self.steer_motor_encoder.getPosition(),
        )

    def getPose(self):
        return self.module_pose

    def setDesiredState(self, newState):
        """
        Updates the current desired state,
        where we want this module to now point.
        """
        # Optimize the input command to reduce unneeded motion.
        optimizedState = kinematics.SwerveModuleState.optimize(
            newState, self.getCurrentState().angle
        )

        deltaAngle = (
            newState.angle - self.desiredState.angle
        )  # The change from the old angle, to the new angle

        self.angleSum = (
            self.angleSum + deltaAngle.radians()
        )  # The sum of all the previous movements up to this point

        # If the target is more than a full rotation away from the actual
        # rotation of the wheel, remove a rotation from the target. This
        # does not change the target angle as it removes one rotations, but
        # prevents the wheel from trying to play catch up
        if RobotBase.isReal():
            if self.angleSum - (2 * math.pi) > self.radians:
                self.angleSum = self.angleSum - (2 * math.pi)
            elif self.angleSum + (2 * math.pi) < self.radians:
                self.angleSum = self.angleSum + (2 * math.pi)

        if self.joy.getRawAxis(1) >= 0.05 or self.joy.getRawAxis(2) >= 0.05:
            currentRef = self.angleSum / (
                2 * math.pi
            )  # The sum (radians) converted to rotations (of the steer wheel)

            # Set the position of the neo to the desired position
            # self.steer_motor.set(0.5)
            self.steer_PID.setReference(
                currentRef, CANSparkMaxLowLevel.ControlType.kPosition
            )

            self.desiredState = newState

    def getCurrentState(self):
        """
        Returns the current state of this module.
        """
        # Current position of the motor encoder (in rotations)
        self.encoder = self.steer_motor_encoder.getPosition()

        # if self.constants["steer_id"] == 1:
        # print(encoder)

        # Divide encoder by ratio of encoder rotations to wheel rotations, times 2pi
        self.radians = self.encoder * (math.pi * 2)

        # Construct a rotation2d object
        self.rot = geometry.Rotation2d(self.radians)

        # The current state is constructed
        # TODO: Measure speed
        current_state = kinematics.SwerveModuleState(0, self.rot)

        # Return
        return current_state

    def getTargetHeading(self):
        """
        Returns the current heading of
        this module.
        """

        return self.desiredState.angle.radians()
