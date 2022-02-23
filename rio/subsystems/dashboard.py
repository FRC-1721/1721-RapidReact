# FRC 1721
# 2022

from commands2 import SubsystemBase

from networktables import NetworkTables

from wpilib import Timer, PowerDistribution

from constants.constants import getConstants


class Dashboard(SubsystemBase):
    """
    This class interfaces quite neatly with
    the companion dashboard code, primarily
    it handles periodic reporting on entries and
    components that do not directly have relation
    to a subsystem.
    """

    def __init__(self):
        super().__init__()

        # Get hardware constants
        self.constants = getConstants("networktables")

        # Background timer
        self.backgroundTimer = Timer()
        self.backgroundTimer.start()

        # Setup hardware
        self.pdp = PowerDistribution()

        # Get an instance of networktables
        self.nt = NetworkTables.getDefault()

        # Get the root table
        self.sd = self.nt.getTable(self.constants["root_table"])

        # Setup subtables
        self.panel_table = self.sd.getSubTable(self.constants["panel_table"])

        # Setup all of the networktable entries
        self.pdp_voltage_entry = self.panel_table.getEntry("voltage")
        self.pdp_current_entry = self.panel_table.getEntry("totalCurrent")

        self.channel_entries = [
            pdpChanInterface(self.panel_table, self.pdp, i) for i in range(16)
        ]

    def periodic(self):
        # Only continue once every 5 seconds.
        if self.backgroundTimer.advanceIfElapsed(1):
            self.pdp_voltage_entry.setDouble(self.pdp.getVoltage())
            self.pdp_current_entry.setDouble(self.pdp.getTotalCurrent())

            for chan in self.channel_entries:
                chan.update()


class pdpChanInterface:
    def __init__(self, table, pdp, chan) -> None:
        self.entry = table.getEntry(f"chan{chan}")
        self.chan = chan
        self.pdp = pdp

    def update(self):
        self.entry.setDouble(self.pdp.getCurrent(self.chan))
