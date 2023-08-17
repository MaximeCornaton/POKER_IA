# Description: Enum for player actions
# Author: Maxime Cornaton
# Date: 2023

from enum import Enum


class PlayerAction(Enum):

    """
    _summary_ : Enum for player actions.
    _description_ : This enum is used to represent the different actions a player can take.
    """

    FOLD = 'fold'
    CHECK = 'check'
    CALL = 'call'
    BET = 'bet'
    RAISE = 'raise'
    ALL_IN = 'all_in'
