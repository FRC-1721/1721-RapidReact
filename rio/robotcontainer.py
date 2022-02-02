import wpilib

import commands2
import commands2.button

# Commands
from commands.flybywire import FlyByWire

# Subsystens
from subsystems.drivetrain import Drivetrain

# Constants
from constants.constants import getConstants


class RobotContainer:
    """
    The bulk of the robot should be declared here, but little logic should be done.
    Logic and interfacing with hardware belongs in subsystems/ and commands/.
    """

    def __init__(self) -> None:
        # Setup constants
        self.constants = getConstants("robot_controls")

        # The driver's controller
        self.driverController = wpilib.Joystick(
            self.constants["mode_a"]["driver"]["driverstation_port"]
        )

        # The robot's subsystems
        self.drivetrain = Drivetrain()

        self.configureButtonBindings()

        # set up default drive command
        self.drivetrain.setDefaultCommand(
            FlyByWire(
                self.drivetrain,
                lambda: -self.driverController.getRawAxis(1),
                lambda: self.driverController.getRawAxis(2),
                lambda: self.driverController.getRawAxis(0),
            )
        )

    def configureButtonBindings(self):
        """
        Use this method to define your button->command mappings. Buttons can be created by
        instantiating a :GenericHID or one of its subclasses (Joystick or XboxController),
        and then passing it to a JoystickButton.
        """
        pass

    def getAutonomousCommand(self) -> commands2.Command:
        return self.chooser.getSelected()
