import wpilib
import wpilib.drive

class UnnamedToaster(wpilib.TimedRobot):

    def robotInit(self):
        self.leftMotorOne = wpilib.Spark(2) #TODO: FIX  THIS
        self.rightMortorOne = wpilib.Spark(4) #These take PWM
        self.leftMotorTwo = wpilib.Spark(1) #values, use the spark
        self.rightMotorTwo = wpilib.Spark(3) # in robotpy-rev
                                            #https://robotpy.readthedocs.io/projects/rev/en/stable/rev/CANSparkMax.html#rev.CANSparkMax
        self.leftSide = wpilib.SpeedControllerGroup(
            self.leftMotorOne, self.leftMotorTwo)
        self.rightSide = wpilib.SpeedControllerGroup(
            self.rightMortorOne, self.rightMotorTwo)

        self.driveTrain = wpilib.drive.DifferentialDrive(
            self.leftSide, self.rightSide)

        self.joy = wpilib.Joystick(0)
    
    def teleopPeriodic(self):
        self.driveTrain.arcadeDrive(0.5,0.5,True)


if __name__ == "__main__":
    wpilib.run(UnnamedToaster)
