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
from commands.swing import Swing

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
from autonomous.driveauto import DriveAuto


class RobotContainer:
    """
    The bulk of the robot should be declared here, but little logic should be done.
    Logic and interfacing with hardware belongs in subsystems/ and commands/.
    """

    def __init__(self) -> None:
        # Setup constants
        controlConsts = getConstants("robot_controls")
        hardConsts = getConstants("robot_hardware")

        # Configure simulated controls, replacing real controls for alternative
        # mappings when in sim mode.
        self.controlDriver = controlConsts["mode_a"]["driver"]
        self.controlOperator = controlConsts["mode_a"]["operator"]
        if not wpilib.RobotBase.isReal():
            # Override the controlMode with simulated controls if we're in the matrix
            self.controlDriver = controlConsts["mode_a"]["sim"]
            self.controlOperator = controlConsts["mode_a"]["sim"]

        # The driver's controller
        self.driverController = wpilib.Joystick(self.controlDriver["controller_port"])
        self.operatorController = wpilib.Joystick(
            self.controlOperator["controller_port"]
        )

        self.yokeConsts = hardConsts["yoke"]

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
                    self.controlDriver["forward_axis"]
                ),
                lambda: self.driverController.getRawAxis(
                    self.controlDriver["steer_axis"]
                ),
                lambda: self.driverController.getRawAxis(
                    self.controlDriver["strafe_axis"]
                ),
            )
        )

        self.climber.setDefaultCommand(
            Climb(
                self.climber,
                self.yoke,
                lambda: self.operatorController.getRawAxis(
                    self.controlOperator["climb_axis"]
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
            self.operatorController, self.controlOperator["kicker_button"]
        ).whenPressed(Kicker(self.yoke))

        commands2.button.JoystickButton(
            self.operatorController, self.controlOperator["intake_button"]
        ).whileHeld(Intake(self.yoke))

        # Triggers the catapult command but its low
        commands2.button.JoystickButton(
            self.operatorController, self.controlOperator["catapult_button"]
        ).whileHeld(
            Catapult(
                self.yoke,
                self.yokeConsts["low_target_speed"],
                self.yokeConsts["low_target_angle"],
            )
        )

        # Triggers the catapult command but its high
        commands2.button.JoystickButton(
            self.operatorController, self.controlOperator["high_catapult_button"]
        ).whileHeld(
            Catapult(
                self.yoke,
                self.yokeConsts["high_target_speed"],
                self.yokeConsts["high_target_angle"],
            )
        )

        # Rezero the swerve modules
        commands2.button.JoystickButton(
            self.driverController, self.controlDriver["rezero_swerve"]
        ).whenPressed(ZeroSwerveModules(self.drivetrain, True))

        commands2.button.POVButton(self.operatorController, 4).whileHeld(
            LimeAuto(self.drivetrain)
        )

        commands2.button.JoystickButton(self.operatorController, 2).whenHeld(
            Swing(self.yoke)
        )

        # Use the menu button to enter climb mode
        # while the yaml file has the climb mode button in it
        # don't use it, it breaks the code
        # commands2.button.JoystickButton(self.operatorController, 7).whileHeld(
        #     Climb(
        #         self.climber,
        #         self.drivetrain,
        #         lambda: self.operatorController.getRawAxis(
        #             self.controlOperator["climb_up"]
        #         ),
        #         lambda: self.operatorController.getRawAxis(
        #             self.controlOperator["climb_down"]
        #         ),
        #     )
        # )

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
        self.autoChooser.addOption("Drive Auto", DriveAuto(self.drivetrain))
        # Put the chooser on the dashboard
        wpilib.SmartDashboard.putData("Autonomous", self.autoChooser)

    def getAutonomousCommand(self) -> commands2.Command:
        return self.autoChooser.getSelected()
