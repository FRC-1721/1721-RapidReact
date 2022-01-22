import wpilib
import wpilib.drive
import rev


class UnnamedToaster(wpilib.TimedRobot):
    def robotInit(self):

        # Initialize port side drive train
        # Port wheel
        self.portMotorLeader = rev.CANSparkMax(2, rev.MotorType.kBrushless)
        self.portMotorFollower = rev.CANSparkMax(1, rev.MotorType.kBrushless)

        # Starboard wheel
        self.starboardMotorOne = rev.CANSparkMax(4, rev.MotorType.kBrushless)
        self.starboardMotorTwo = rev.CANSparkMax(3, rev.MotorType.kBrushless)

        self.portMotorFollower.follow(self.portMotorLeader)
        self.starboardMotorTwo.follow(self.starboardMotorOne)

        self.driveTrain = wpilib.drive.DifferentialDrive(
            self.portMotorLeader, self.starboardMotorOne)

        self.joy = wpilib.Joystick(0)

    # Initalizes joystick to control the drivetrain
    def teleopPeriodic(self):
        self.driveTrain.arcadeDrive(
            self.joy.getRawAxis(1), -self.joy.getRawAxis(2))


if __name__ == "__main__":
    wpilib.run(UnnamedToaster)
