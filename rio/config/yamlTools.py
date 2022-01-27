# Tidal Force Robotics
# 2022
# MIT License

import yaml


class RobotConfiguration:
    def __init__(self):
        """
        Constructs a RobotConfiguration (a custom class)
        we can use to query for yaml database values.
        """

        with open("config/robot_dimensions.yaml", "r") as robot_dimms:
            self.dimms = yaml.safe_load(robot_dimms)
