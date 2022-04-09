#!/usr/bin/env python3

import json
import typing
import wpilib
import commands2

from robotcontainer import RobotContainer
from datetime import datetime
from wpilib import RobotBase, deployinfo
from networktables import NetworkTables


class BurntToaster(commands2.TimedCommandRobot):
    """
    Our default robot class, pass it to wpilib.run

    Command v2 robots are encouraged to inherit from TimedCommandRobot, which
    has an implementation of robotPeriodic which runs the scheduler for you
    """

    autonomousCommand: typing.Optional[commands2.Command] = None

    def robotInit(self) -> None:
        """
        This function is run when the robot is first started up and should be used for any
        initialization code.
        """

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("--------------------------------------------------------------")
        print("RESTARTING ROBOT AT ", current_time)
        print("--------------------------------------------------------------")

        # Instantiate our RobotContainer.  This will perform all our button bindings, and put our
        # autonomous chooser on the dashboard.
        self.container = RobotContainer()

        # Deploy data, created at deploytime
        self.deploy_data = self.getDeployData()

        # Configure networktables
        self.configureNetworktables()

        # Setup our misc/background timer.
        self.addPeriodic(self.extraInfo, 2.5)

    def disabledInit(self) -> None:
        """This function is called once each time the robot enters Disabled mode."""

    def disabledPeriodic(self) -> None:
        """This function is called periodically when disabled"""

    def autonomousInit(self) -> None:
        """This autonomous runs the autonomous command selected by your RobotContainer class."""
        self.autonomousCommand = self.container.getAutonomousCommand()

        if self.autonomousCommand:
            self.autonomousCommand.schedule()

        # Trigger an enabledInit()
        self.container.enabledInit()

    def autonomousPeriodic(self) -> None:
        """This function is called periodically during autonomous"""

    def teleopInit(self) -> None:
        # This makes sure that the autonomous stops running when
        # teleop starts running. If you want the autonomous to
        # continue until interrupted by another command, remove
        # this line or comment it out.
        if self.autonomousCommand:
            self.autonomousCommand.cancel()

        # Trigger an enabledInit()
        self.container.enabledInit()

    def teleopPeriodic(self) -> None:
        """This function is called periodically during operator control"""

    def testInit(self) -> None:
        # Cancels all running commands at the start of test mode
        commands2.CommandScheduler.getInstance().cancelAll()

        # Trigger an enabledInit()
        # self.container.enabledInit()

    def _simulationPeriodic(self) -> None:
        """Called during simulation after the rest of the code has excecuted."""

    def testPeriodic(self) -> None:
        """Called every time during test mode"""

    def extraInfo(self) -> None:
        """
        Called by a TimedRobot timer, contianing data that should not change much
        but should be kept current on networktables or other connectors.

        This is kind of a catchall/misc method, runs every 2 or so seconds.
        """

        data = self.getDeployData()

        for key in data:
            key_entry = self.build_table.getEntry(str(key))
            key_entry.setString(str(data[key]))

    def getDeployData(self):
        """
        Returns appropriate deploy data.
        """

        fakedata = {
            "git-desc": "week0-69-g42096-dirty",
            "git-branch": "sim/sim",
            "deploy-host": "SimulatedLaptop",
            "deploy-user": "SimUser",
            "code-path": "/sim/simulatedrobot",
            "deploy-date": "never",
        }

        if RobotBase.isReal():
            try:
                with open("/home/lvuser/py/deploy.json") as fp:
                    return json.load(fp)
            except FileNotFoundError:
                return fakedata
        else:
            return fakedata

    def configureNetworktables(self):
        # Configure networktables
        self.nt = NetworkTables.getDefault()
        self.sd = self.nt.getTable("SmartDashboard")

        # Subtables
        self.build_table = self.sd.getSubTable("BuildData")


if __name__ == "__main__":
    wpilib.run(BurntToaster)
