from commands2 import SubsystemBase
from wpilib import SpeedControllerGroup, CANSparkMax, Encoder, AnalogGyro
from wpilib.drive import DifferentialDrive
from wpimath.geometry import Pose2d, Rotation2d
from wpimath.kinematics import DifferentialDriveOdometry, DifferentialDriveWheelSpeeds
from constants.constants import getConstants


class AutoSwerve(SubsystemBase):
    def __init__(self):

        super().__init__()

        constants = getConstants("robot_hardware")
        self.drive_const = constants["drivetrain"]
        self.pid_const = constants["pid"]

        # Create swerve drive modules
        # Fore port module
        self.fp_module = SpeedControllerGroup(
            self.drive_const["fp_module"]["drive_id"],
            self.drive_const["fp_module"]["steer_id"],
        )
        # Fore starboard module
        self.fs_module = SpeedControllerGroup(
            self.drive_const["fs_module"]["drive_id"],
            self.drive_const["fs_module"]["steer_id"],
        )

        # Aft port module
        self.ap_module = SpeedControllerGroup(
            self.drive_const["ap_module"]["drive_id"],
            self.drive_const["ap_module"]["steer_id"],
        )
        # Aft starboard module
        self.as_module = SpeedControllerGroup(
            self.drive_const["as_module"]["drive_id"],
            self.drive_const["as_module"]["steer_id"],
        )

        # orgonizes motors into sides (might be a bad idea)
        self.leftMotors = self.fp_module, self.fs_module
        self.rightMotors = self.ap_module, self.as_module

        # TODO replace DifferentialDrive with our custom swerve drive
        self.drive = DifferentialDrive(self.leftMotors, self.rightMotors)

        # Create the encoder objects.
        self.fp_encoder = Encoder(self.pid_const["drive"], self.pid_const["steer"])
        self.fs_encoder = Encoder(self.pid_const["drive"], self.pid_const["steer"])
        self.ap_encoder = Encoder(self.pid_const["drive"], self.pid_const["steer"])
        self.as_encoder = Encoder(self.pid_const["drive"], self.pid_const["steer"])

        # Configure the encoder so it knows how many encoder units are in one rotation.
        # enc/encs = encoder/encoders
        # fp encodersself.ap_enc_steer
        self.fp_enc_drive.setDistancePerPulse(self.pid_const["drive"]["ratio"])
        self.fp_enc_steer.setDistancePerPulse(self.pid_const["steer"]["ratio"])

        # fs encoders
        self.fs_enc_drive.setDistancePerPulse(self.pid_const["drive"]["ratio"])
        self.fs_enc_steer.setDistancePerPulse(self.pid_const["steer"]["ratio"])

        # ap encoders
        self.ap_enc_drive.setDistancePerPulse(self.pid_const["drive"]["ratio"])
        self.ap_enc_steer.setDistancePerPulse(self.pid_const["steer"]["ratio"])

        # as encoders
        self.as_enc_drive.setDistancePerPulse(self.pid_const["drive"]["ratio"])
        self.as_enc_steer.setDistancePerPulse(self.pid_const["steer"]["ratio"])

        # orgonize the encoders (might be a bad idea)
        self.fp_encs = self.fp_enc_drive, self.fp_enc_steer
        self.fs_encs = self.fs_enc_drive, self.fs_enc_steer
        self.ap_encs = self.ap_enc_drive, self.ap_enc_steer
        self.as_encs = self.as_enc_drive, self.as_enc_steer

        self.leftEncoder = self.fp_encs, self.fs_encs
        self.rightEncoder = self.ap_encs, self.as_encs

        # Create the gyro, a sensor which can indicate the heading of the robot relative
        # to a customizable position.
        self.gyro = AnalogGyro(1)

        # Create the an object for our odometry, which will utilize sensor data to
        # keep a record of our position on the field.
        # TODO replace DifferentialDriveOdometry with our custom odometry
        self.odometry = DifferentialDriveOdometry(self.gyro.getRotation2d())

        # Reset the encoders upon the initilization of the robot.
        self.resetEncoders()

    def periodic(self):
        """
        Called periodically when it can be called. Updates the robot's
        odometry with sensor data.
        """
        self.odometry.update(
            self.gyro.getRotation2d(),
            self.leftEncoder.getDistance(),
            self.rightEncoder.getDistance(),
        )

    def getPose(self):
        """Returns the current position of the robot using it's odometry."""
        return self.odometry.getPose()

    def getWheelSpeeds(self):
        """Return an object which represents the wheel speeds of our drivetrain."""
        speeds = DifferentialDriveWheelSpeeds(
            self.leftEncoder.getRate(), self.rightEncoder.getRate()
        )
        return speeds

    def resetOdometry(self, pose):
        """Resets the robot's odometry to a given position."""
        self.resetEncoders()
        self.odometry.resetPosition(pose, self.gyro.getRotation2d())

    def arcadeDrive(self, fwd, rot):
        """Drive the robot with standard arcade controls."""
        self.drive.arcadeDrive(fwd, rot)

    def tankDriveVolts(self, leftVolts, rightVolts):
        """Control the robot's drivetrain with voltage inputs for each side."""
        # Set the voltage of the left side.
        self.leftMotors.setVoltage(leftVolts)

        # Set the voltage of the right side. It's
        # inverted with a negative sign because it's motors need to spin in the negative direction
        # to move forward.
        self.rightMotors.setVoltage(-rightVolts)

        # Resets the timer for this motor's MotorSafety
        self.drive.feed()

    def resetEncoders(self):
        """Resets the encoders of the drivetrain."""
        self.leftEncoder.reset()
        self.rightEncoder.reset()

    def getAverageEncoderDistance(self):
        """
        Take the sum of each encoder's traversed distance and divide it by two,
        since we have two encoder values, to find the average value of the two.
        """
        return (self.leftEncoder.getDistance() + self.rightEncoder.getDistance()) / 2

    def getLeftEncoder(self):
        """Returns the left encoder object."""
        return self.leftEncoder

    def getRightEncoder(self):
        """Returns the right encoder object."""
        return self.rightEncoder

    def setMaxOutput(self, maxOutput):
        """Set the max percent output of the drivetrain, allowing for slower control."""
        self.drive.setMaxOutput(maxOutput)

    def zeroHeading(self):
        """Zeroes the gyro's heading."""
        self.gyro.reset()

    def getHeading(self):
        """Return the current heading of the robot."""
        return self.gyro.getRotation2d().getDegrees()

    def getTurnRate(self):
        """Returns the turning rate of the robot using the gyro."""

        # The minus sign negates the value.
        return -self.gyro.getRate()
