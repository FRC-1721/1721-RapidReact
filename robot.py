import wpilib
import wpilib.drive
import rev

class UnnamedToaster(wpilib.TimedRobot):
    
    def robotInit(self):
        self.leftMotorOne = rev.CANSparkMax(self, 2, rev.MotorType.kBrushless)
        self.leftMotorTwo = rev.CANSparkMax(self, 1, rev.MotorType.kBrushless)
        self.rightMotorOne = rev.CANSparkMax(self, 4, rev.MotorType.kBrushless)
        self.rightMotorTwo = rev.CANSparkMax(self, 3, rev.MotorType.kBrushless)

        self.leftMotorTwo.follow(self.leftMotorOne)
        self.rightMotorTwo.follow(self.RightMotorOne)

        self.driveTrain = wpilib.drive.DifferentialDrive(
            self.leftMotorOne, self.rightMotorOne)

        self.joy = wpilib.Joystick(0)

    def teleopPeriodic(self):
        self.driveTrain.arcadeDrive(self.joy.getX, self.joy.getY)


if __name__ == "__main__":
    wpilib.run(UnnamedToaster)
