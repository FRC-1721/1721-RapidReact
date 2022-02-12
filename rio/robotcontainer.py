import wpilib

import commands2
import commands2.button

# Commands
from commands.flybywire import FlyByWire

# Subsystens
from subsystems.drivetrain import Drivetrain
from subsystems.lighting import Lighting

# Constants
from constants.constants import getConstants

# Auto
from commands.nullauto import NullAuto


class RobotContainer:
    """
    The bulk of the robot should be declared here, but little logic should be done.
    Logic and interfacing with hardware belongs in subsystems/ and commands/.
    """

    def __init__(self) -> None:
        # Setup constants
        controlConsts = getConstants("robot_controls")

        # Configure simulated controls, replacing real controls for alternative
        # mappings when in sim mode.
        self.controlMode = controlConsts["mode_a"]["driver"]
        if not wpilib.RobotBase.isReal():
            # Override the controlMode with simulated controls if we're in the matrix
            self.controlMode = controlConsts["mode_a"]["sim"]

        # The driver's controller
        self.driverController = wpilib.Joystick(self.controlMode["controller_port"])

        # The robot's subsystems
        self.drivetrain = Drivetrain()
        self.lighting = Lighting()

        # Configure button bindings
        self.configureButtonBindings()

        # Setup all autonomous routines
        self.configureAutonomous()

        # set up default drive command
        self.drivetrain.setDefaultCommand(
            FlyByWire(
                self.drivetrain,
                lambda: -self.driverController.getRawAxis(
                    self.controlMode["forward_axis"]
                ),
                lambda: self.driverController.getRawAxis(
                    self.controlMode["steer_axis"]
                ),
                lambda: self.driverController.getRawAxis(
                    self.controlMode["strafe_axis"]
                ),
            )
        )

    def configureButtonBindings(self):
        """
        Use this method to define your button->command mappings. Buttons can be created by
        instantiating a :GenericHID or one of its subclasses (Joystick or XboxController),
        and then passing it to a JoystickButton.
        """
        pass

    def configureAutonomous(self):
        # Create a sendable chooser
        self.autoChooser = wpilib.SendableChooser()

        # Add options for chooser
        self.autoChooser.setDefaultOption("Null Auto", NullAuto(self.drivetrain))

        # Put the chooser on the dashboard
        wpilib.SmartDashboard.putData("Autonomous", self.autoChooser)

    def getAutonomousCommand(self) -> commands2.Command:
        return self.autoChooser.getSelected()
