# Description: Reward manager for the game
# Author: Maxime Cornaton
# Date: 2023

from environment.cHistory import History
from environment.cPlayer import Player
from environment.cPokerGame import PokerGame


""" 
_summary_ : Calculate the reward.
_description_ : This method is used to calculate the reward.    
_attributes_ :
    - game : Game of poker.
    - winners : Winners of the game.
_returns_ : Round rewards and game rewards.
"""


def add_reward(game: PokerGame, winners: [Player]) -> ([int], [int]):
    history = game.history.get()
    for round in history:
        for event in round['events']:
            if event['player'] in winners:
                event['round_rewards'] = event['amount']
            else:
                event['round_rewards'] = -event['amount']
            event['game_rewards'] = event['player'].chips

    return history


"""
_summary_ : Create the game data.
_description_ : This method is used to create the game data.
_attributes_ :  
    - game : Game of poker.
    - winners : Winners of the game.
_returns_ : Data of the game.   
"""


def create_game_data(game: PokerGame, winners: [Player]) -> dict:
    data = add_reward(game, winners)

    return data
