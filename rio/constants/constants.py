# Tidal Force Robotics
# 2022

import os
from sre_constants import CATEGORY_WORD
from wpilib import RobotBase
import yaml
import logging

"""
Use this file only for storing non-changing constants.
"""


def getConstants(identifier):
    constants = {}

    # Clunky but it works
    if RobotBase.isReal():
        path = "/home/lvuser/py/constants/"
    else:
        path = "constants/"

    try:
        # Try opening requested .yaml
        with open(f"{path}{identifier}.yaml", "r") as yamlFile:
            # Use yaml.safe_load to load the yaml into a dict
            constants = yaml.safe_load(yamlFile)
    except FileNotFoundError as e:
        # If the file is not found, report it!
        logging.error(f"{identifier} config not found!")
        raise e

    # When all is done, return the important bits!
    return constants
