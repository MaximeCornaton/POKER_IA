# Description: Helper functions for the project
# Author: Maxime Cornaton
# Date: 2023

import json


"""
_summary_ : Save a json file.
_description_ : This method is used to save a json file.
_attributes_ :  
    - data : Data to save.
    - path : Path of the file.
_returns_ : None
"""


def save_json(data, path: str) -> None:
    with open(path, 'w') as fp:
        json.dump(data, fp, default=make_serializable, indent=4)


"""
_summary_ : Load a json file.
_description_ : This method is used to load a json file.
_attributes_ :
    - path : Path of the file.  
_returns_ : Data of the file.  
"""


def load_json(path: str) -> dict:
    with open(path, 'r') as fp:
        return json.load(fp)


"""
_summary_ : Make an object serializable.
_description_ : This method is used to make an object serializable.
_attributes_ :  
    - obj : Object to make serializable.
_returns_ : Serializable object.
"""


def make_serializable(obj) -> dict:
    return str(obj)
