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


def extract_all_actions(data: dict) -> dict:
    newData = {
        "rounds": [],
        "big_blind": [],
        "small_blind": [],
        "pot": [],
        "community_cards": [],
        "num_players": [],
        "own_stack": [],
        "own_cards": [],
        # "opponent_stacks": [],
        "actions": [],
        "amount": [],
        "round_rewards": [],
        "game_rewards": []
    }

    for round in data:
        for i, event in enumerate(round['events']):
            newData['rounds'].append(round['round'])
            newData['big_blind'].append(round['big_blind'])
            newData['small_blind'].append(round['small_blind'])
            newData['pot'].append(round['pot'])
            newData['community_cards'].append(round['community_cards'])
            newData['num_players'].append(len(round['players_state']))
            newData['own_stack'].append(round['players_state'][i]['stack'])
            newData['own_cards'].append(round['players_state'][i]['cards'])
            # newData['opponent_stacks'].append(player_state['opponent_stacks'])
            newData['actions'].append(event['action'])
            newData['amount'].append(event['amount'])
            newData['round_rewards'].append(event['round_rewards'])
            newData['game_rewards'].append(event['game_rewards'])

    return newData


"""
_summary_ : Transform the game data.
_description_ : This method is used to transform the game data.
_attributes_ :
    - game : Game of poker.
    - winners : Winners of the game.
_returns_ : Game data.
"""


def preprocess_game_data(game: PokerGame, winners: [Player]) -> dict:
    data = add_reward(game, winners)
    data = extract_all_actions(data)

    return data
