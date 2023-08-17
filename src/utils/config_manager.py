# Description: This file contains the functions to manage the configuration.
# Author: Maxime Cornaton
# Date: 2023

import json


""" 
_summary_ : Load the configuration. 
_description_ : This method is used to load the configuration.
_attributes_ :
    - config_filename : Name of the configuration file.
_returns_ : Configuration.
"""


def load_config(config_filename):
    with open(config_filename, 'r') as f:
        config = json.load(f)
    return config
