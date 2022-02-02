# Tidal Force Robotics
# 2022

import yaml
import logging

"""
Use this file only for storing non-changing constants.
"""


def getConstants(identifier):
    constants = {}

    try:
        # Try opening requested .yaml
        with open(f"constants/{identifier}.yaml", "r") as yamlFile:
            # Use yaml.safe_load to load the yaml into a dict
            constants = yaml.safe_load(yamlFile)
    except FileNotFoundError as e:
        # If the file is not found, report it!
        logging.error(f"{identifier} config not found!")
        raise e

    # When all is done, return the important bits!
    return constants
