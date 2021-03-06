import math
import commands2

from networktables import NetworkTables
from commands.flybywire import FlyByWire


class LimeAuto(commands2.CommandBase):
    def __init__(self, drivetrain) -> None:
        """
        Points the robot towards any seen limelight targets
        """
        super().__init__()

        # Get drivetrain class
        self.drivetrain = drivetrain
        self.addRequirements([self.drivetrain])

        # Configure networktable tables
        self.lime_angle = 0
        self.nt = NetworkTables.getDefault()
        self.lime_table = self.nt.getTable("SmartDashboard")

        # Get tables from network tables
        self.target_seen = self.lime_table.getEntry("tv")
        self.horisontal_diff = self.lime_table.getEntry("tx")

        # Set the LimeLight pipeline to 0 (limelight off)
        self.lime_table.putNumber("pipeline", 0)

    def execute(self) -> None:
        # set the LimeLight pipeline to 1 (Limelight on)
        self.lime_table.putNumber("pipeline", 1)
        print("Lime executing")

        # If a vision target is spotted by the limelight
        if self.target_seen:
            print("TARGET SPOTTED")
            # Get the current rotation of the robot
            current_angle = self.drivetrain.getRotation().radians()

            # If the vision target is to the right, rotate clockwise
            if self.horisontal_diff > 5:
                self.drivetrain.arcadeDrive(0, 0, current_angle - 0.1)
                print("TARGET TO THE RIGHT")

            # If the vision target is to the left, rotate counter clockwise
            elif self.horisontal_diff < 5:
                self.drivetrain.arcadeDrive(0, 0, current_angle + 0.1)
                print("TARGET TO THE LEFT")

            # If the vision target is in the center, dont move
            else:
                self.drivetrain.arcadeDrive(0, 0, current_angle)
                print("TARGET LOCKED")

    def isFinished(self) -> bool:

        # Set the LimeLight pipeline to 0 (limelight off)
        self.lime_table.putNumber("pipeline", 0)

        return True
