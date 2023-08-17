# Description: History class for saving the history of the game
# Author: Maxime Cornaton
# Date: 2023

import json


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
        self.history = {
            'states': [],
            'players': [],
            'actions': [],
            'amounts': [],
        }

    """
    _summary_ : Add a new entry to the history.
    _description_ : This method is used to add a new entry to the history.
    _attributes_ :
        - state : State of the game.
        - player : Player who made the action.
        - action : Action made by the player.
        - amount : Amount of the action.
    _returns_ : None
    """

    def add(self, state, player, action, amount: int) -> None:
        self.history['states'].append(state)
        self.history['players'].append(player)
        self.history['actions'].append(action)
        self.history['amounts'].append(amount)

    """ 
    _summary_ : Get the history.
    _description_ : This method is used to get the history.
    _attributes_ : None
    _returns_ : History of the game.
    """

    def get(self) -> dict:
        return self.history['states'], self.history['players'], self.history['actions'], self.history['amounts']

    """
    _summary_ : Save the history.
    _description_ : This method is used to download the history.
    _attributes_ :
        - path : Path to save the history.
    _returns_ : None
    """

    def save(self, path: str) -> None:
        history = {
            'states': self.history['states'],
            'player': [str(player) for player in self.history['players']],
            'actions': [action.name for action in self.history['actions']],
            'amounts': self.history['amounts'],
        }

        with open(path, 'w') as f:
            json.dump(history, f, indent=2)
