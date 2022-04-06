import wpilib

import commands2
import commands2.button

# Commands
from commands.flybywire import FlyByWire
from commands.test_button_action import TestButtonAction
from commands.kicker_button import Kicker
from commands.intake import Intake
from commands.catapult import Catapult
from commands.zero_swerve import ZeroSwerveModules
from commands.climb import Climb

# from commands.fake_trigger import FakeTrigger
from commands.lime_detect import LimeAuto

# Triggers
from commands.triggers.trigger_trigger import Trigger

# Subsystens
from subsystems.drivetrain import Drivetrain
from subsystems.yoke import Yoke
from subsystems.climber import Climber

# Constants
from constants.constants import getConstants

# Autonomous
from autonomous.conversion_test import ConversionTest
from commands.nullauto import NullAuto
from autonomous.botchauto import BotchAuto
from autonomous.highBotchAuto import HighBotchAuto


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
        self.climber = Climber()
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

    def configureButtonBindings(self):
        """
        Use this method to define your button->command mappings. Buttons can be created by
        instantiating a :GenericHID or one of its subclasses (Joystick or XboxController),
        and then passing it to a JoystickButton.
        """

        commands2.button.JoystickButton(
            self.driverController, self.controlMode["kicker_button"]
        ).whenPressed(Kicker(self.yoke))

        commands2.button.JoystickButton(
            self.driverController, self.controlMode["intake_button"]
        ).whileHeld(Intake(self.yoke))

        # Triggers the catapult command but its low
        commands2.button.JoystickButton(
            self.driverController, self.controlMode["catapult_button"]
        ).whileHeld(Catapult(self.yoke, 85, 0.25))

        # Triggers the catapult command but its high
        commands2.button.JoystickButton(
            self.driverController, self.controlMode["high_catapult_button"]
        ).whileHeld(Catapult(self.yoke, 80, 0.5))

        # Rezero the swerve modules
        commands2.button.JoystickButton(
            self.driverController, self.controlMode["rezero_swerve"]
        ).whenPressed(ZeroSwerveModules(self.drivetrain, True))

        commands2.button.POVButton(self.driverController, 4).whileHeld(
            LimeAuto(self.drivetrain)
        )

        # Use the menu button to enter climb mode
        commands2.button.JoystickButton(self.driverController, 7).whileHeld(
            Climb(
                self.climber,
                self.drivetrain,
                lambda: self.driverController.getRawAxis(5),
                lambda: self.driverController.getRawAxis(
                    self.controlMode["strafe_axis"]
                ),
            )
        )

    def enabledInit(self):
        """
        Idea from FRC discord, called any time
        we move to enabled.
        """

        if not self.drivetrain.all_zeroed():
            ZeroSwerveModules(self.drivetrain).schedule()

    def configureAutonomous(self):
        # Create a sendable chooser
        self.autoChooser = wpilib.SendableChooser()

        # Add options for chooser
        # self.autoChooser.setDefaultOption("Null Auto", NullAuto(self.drivetrain))
        self.autoChooser.setDefaultOption(
            "(Comp) Low Goal", BotchAuto(self.yoke, self.drivetrain)
        )
        self.autoChooser.addOption(
            "(Comp) High Cal", HighBotchAuto(self.yoke, self.drivetrain)
        )
        self.autoChooser.addOption("(Dev) Null Auto", NullAuto(self.drivetrain))
        self.autoChooser.addOption(
            "(Dev) Conversion Test", ConversionTest(self.drivetrain)
        )

        # Put the chooser on the dashboard
        wpilib.SmartDashboard.putData("Autonomous", self.autoChooser)

    def getAutonomousCommand(self) -> commands2.Command:
        return self.autoChooser.getSelected()
