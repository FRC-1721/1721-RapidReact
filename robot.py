import wpilib
import wpilib.drive
import rev

class UnnamedToaster(wpilib.TimedRobot):
    
    def robotInit(self):
        self.leftMotorOne = rev.CANSparkMax(2, rev.MotorType.kBrushless)
        self.leftMotorTwo = rev.CANSparkMax(1, rev.MotorType.kBrushless)
        self.rightMotorOne = rev.CANSparkMax(4, rev.MotorType.kBrushless)
        self.rightMotorTwo = rev.CANSparkMax(3, rev.MotorType.kBrushless)

        self.leftMotorTwo.follow(self.leftMotorOne)
        self.rightMotorTwo.follow(self.rightMotorOne)

        self.driveTrain = wpilib.drive.DifferentialDrive(
            self.leftMotorOne, self.rightMotorOne)

        self.joy = wpilib.Joystick(0)

    def teleopPeriodic(self):
       self.driveTrain.arcadeDrive(self.joy.getX, self.joy.getY, false)


if __name__ == "__main__":
    wpilib.run(UnnamedToaster)
