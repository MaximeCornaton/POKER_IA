# Description: History class for saving the history of the game
# Author: Maxime Cornaton
# Date: 2023

import json

from environment.cPlayer import Player
from environment.ePlayerAction import PlayerAction
from utils.helpers import save_json


class History:

    """
    _summary_ : Class used to save the history of the game.
    _description_ : This class is used to save the history of the game.
    _attributes_ :
        - history : History of the game.
    _returns_ : None
    """

    def __init__(self) -> None:
        self.reset()

    """
    _summary_ : Reset the history.
    _description_ : This method is used to reset the history.
    _attributes_ : None
    _returns_ : None
    """

    def reset(self) -> None:
        self.history = [
            # {
            #     'round': 0,
            #     'big_blind': 0,
            #     'small_blind': 0,
            #     'pot': 0,
            #     'community_cards': [],
            #     'players_state': [
            #         {
            #             'player': Player,
            #             'stack': 0,
            #             'cards': []
            #         },
            #     ],
            #     'events': [
            #         {
            #             'player': Player,
            #             'action': PlayerAction,
            #             'amount': 0
            #         },
            #     ]

            # },
        ]

    """
    _summary_ : Add a new entry to the history.
    _description_ : This method is used to add a new entry to the history.
    _attributes_ :
        - round : Round of the game.
        - state : State of the game.
        - decision : Decision of the players
    """

    def add(self, round: int, state: dict, events: dict) -> None:
        self.history.append({
            'round': round,
            'big_blind': state['big_blind'],
            'small_blind': state['small_blind'],
            'pot': state['pot'],
            'community_cards': state['community_cards'].copy(),
            'players_state': state['players_state'].copy(),
            'events': events
        })

    """ 
    _summary_ : Get the history.
    _description_ : This method is used to get the history.
    _attributes_ : None
    _returns_ : History of the game.
    """

    def get(self) -> dict:
        return self.history

    """
    _summary_ : Save the history.
    _description_ : This method is used to download the history.
    _attributes_ :
        - path : Path to save the history.
    _returns_ : None
    """

    def save(self, path: str) -> None:
        save_json(self.history, path)
