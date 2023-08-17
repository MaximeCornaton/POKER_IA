# Description: Reward manager for the game
# Author: Maxime Cornaton
# Date: 2023

from environment.cHistory import History
from environment.cPlayer import Player


""" 
_summary_ : Calculate the reward.
_description_ : This method is used to calculate the reward.    
_attributes_ :
    - history : History of the game.
    - winners : Winners of the game.
_returns_ : Reward of the game.
"""


def calculate_reward(history: History, winners: [Player]) -> int:
    pass
