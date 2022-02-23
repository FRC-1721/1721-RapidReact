import wpilib

import commands2
import commands2.button

# Commands
from commands.flybywire import FlyByWire
from commands.test_button_action import TestButtonAction
from commands.sloppy_intake import SloppyIntake
from commands.kicker_button import Kicker

# Subsystens
from subsystems.drivetrain import Drivetrain
from subsystems.lighting import Lighting
from subsystems.yoke import Yoke

# Constants
from constants.constants import getConstants

# Auto
from commands.nullauto import NullAuto
from commands.botchauto import BotchAuto


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
        self.yoke = Yoke()

        # Configure button bindings
        self.configureButtonBindings()

        # Setup all autonomous routines
        self.configureAutonomous()

        # Setup default commands
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

        # self.yoke.setDefaultCommand(
        #    SloppyIntake(
        #        self.yoke,
        #        lambda: self.driverController.getRawAxis(
        #            self.controlMode["raw_shooter_speed_axis"]
        #        ),
        #        lambda: self.driverController.getRawAxis(
        #            self.controlMode["raw_shooter_intake_axis"]
        #        ),
        #        lambda: self.driverController.getRawAxis(
        #            self.controlMode["raw_shooter_angle_axis"]
        #        ),
        #    )
        # )

    def configureButtonBindings(self):
        """
        Use this method to define your button->command mappings. Buttons can be created by
        instantiating a :GenericHID or one of its subclasses (Joystick or XboxController),
        and then passing it to a JoystickButton.
        """
        # use the A button the xbox controller
        # commands2.button.JoystickButton(self.driverController, 1).whenPressed(
        #    TestButtonAction(self.drivetrain)
        # )

        # use the B button the xbox controller to activate the kicker
        commands2.button.JoystickButton(self.driverController, 5).whenPressed(
            Kicker(self.yoke)
        )

        # use the Y, X, and A buttons to operate the intake
        # TODO: This is test code and kinda bad
        commands2.button.JoystickButton(self.driverController, 4).whileHeld(
            SloppyIntake(self.yoke, True)
        )

        commands2.button.JoystickButton(self.driverController, 1).whileHeld(
            SloppyIntake(self.yoke, False)
        )

    def configureAutonomous(self):
        # Create a sendable chooser
        self.autoChooser = wpilib.SendableChooser()

        # Add options for chooser
        # self.autoChooser.setDefaultOption("Null Auto", NullAuto(self.drivetrain))
        self.autoChooser.setDefaultOption(
            "Caleb pick this one Auto", BotchAuto(self.yoke, self.drivetrain)
        )
        self.autoChooser.addOption("Null Auto", NullAuto(self.drivetrain))

        # Put the chooser on the dashboard
        wpilib.SmartDashboard.putData("Autonomous", self.autoChooser)

    def getAutonomousCommand(self) -> commands2.Command:
        return self.autoChooser.getSelected()
