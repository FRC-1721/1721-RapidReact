import rev
import wpilib
import wpimath
import wpilib.drive


import config.yamlTools as yamlTools


class UnnamedToaster(wpilib.TimedRobot):
    def robotInit(self):

        # Initialize port side drive train
        # Port wheel
        self.portMotorLeader = rev.CANSparkMax(
            2, rev._rev.CANSparkMaxLowLevel.MotorType.kBrushless
        )
        self.portMotorFollower = rev.CANSparkMax(
            1, rev._rev.CANSparkMaxLowLevel.MotorType.kBrushless
        )

        # Starboard wheel
        self.starboardMotorOne = rev.CANSparkMax(
            4, rev._rev.CANSparkMaxLowLevel.MotorType.kBrushless
        )
        self.starboardMotorTwo = rev.CANSparkMax(
            3, rev._rev.CANSparkMaxLowLevel.MotorType.kBrushless
        )

        self.portMotorFollower.follow(self.portMotorLeader)
        self.starboardMotorTwo.follow(self.starboardMotorOne)

        # Experimenting with swerve drive

        self.ForeStarboardSwerveModuleLocation = wpimath.geometry.Translation2d(
            0.5, -0.5
        )
        self.AftStarboardSwerveModuleLocation = wpimath.geometry.Translation2d(
            -0.5, -0.5
        )
        self.ForePortSwerveModuleLocation = wpimath.geometry.Translation2d(0.5, 0.5)
        self.AftPortSwerveModuleLocation = wpimath.geometry.Translation2d(-0.5, 0.5)

        self.swerveDrivetrain = wpimath.kinematics.SwerveDrive4Kinematics(
            self.ForeStarboardSwerveModuleLocation,
            self.AftStarboardSwerveModuleLocation,
            self.ForePortSwerveModuleLocation,
            self.AftPortSwerveModuleLocation,
        )

        self.driveTrain = wpilib.drive.DifferentialDrive(
            self.portMotorLeader, self.starboardMotorOne
        )

        self.joy = wpilib.Joystick(0)

        self.config = yamlTools.RobotConfiguration()

    # Initalizes joystick to control the drivetrain
    def teleopPeriodic(self):
        self.driveTrain.arcadeDrive(self.joy.getRawAxis(1), -self.joy.getRawAxis(2))

        m_chassisSpeeds = wpimath.kinematics.ChassisSpeeds(
            self.joy.getRawAxis(1), self.joy.getRawAxis(0), self.joy.getRawAxis(2)
        )

        fl, fr, bl, br = self.swerveDrivetrain.toSwerveModuleStates(m_chassisSpeeds)

        print(
            f"""Module A
        {fl.speed}
        {fl.angle}
        Module B
        {fr.speed}
        {fr.angle}
        Module C
        {bl.speed}
        {bl.angle}
        Module D
        {br.speed}
        {br.angle}"""
        )

        # print(self.config.dimms)


if __name__ == "__main__":
    wpilib.run(UnnamedToaster)
