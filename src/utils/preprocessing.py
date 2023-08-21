# Description: Reward manager for the game
# Author: Maxime Cornaton
# Date: 2023

import torch
from environment.cHistory import History
from environment.cPlayer import Player
from environment.cPokerGame import PokerGame
from environment.ePlayerAction import PlayerAction

suit_to_int = {
    'None': -1,
    'Spades': 0,
    'Hearts': 1,
    'Diamonds': 2,
    'Clubs': 3,
}

value_to_int = {
    'None': -1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'Jack': 11,
    'Queen': 12,
    'King': 13,
    'Ace': 1
}

action_to_int = {
    PlayerAction.FOLD: 0,
    PlayerAction.CHECK: 1,
    PlayerAction.CALL: 2,
    PlayerAction.BET: 3,
    PlayerAction.RAISE: 4,
    PlayerAction.ALL_IN: 5
}


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
        "community_cards_suit_0": [-1] * len(data[0]['players_state']),
        "community_cards_value_0": [-1] * len(data[0]['players_state']),
        "community_cards_suit_1": [-1] * len(data[0]['players_state']),
        "community_cards_value_1": [-1] * len(data[0]['players_state']),
        "community_cards_suit_2": [-1] * len(data[0]['players_state']),
        "community_cards_value_2": [-1] * len(data[0]['players_state']),
        "community_cards_suit_3": [-1] * len(data[0]['players_state'] * 2),
        "community_cards_value_3": [-1] * len(data[0]['players_state'] * 2),
        "community_cards_suit_4": [-1] * len(data[0]['players_state'] * 3),
        "community_cards_value_4": [-1] * len(data[0]['players_state'] * 3),
        "community_cards_suit_5": [-1] * len(data[0]['players_state'] * 4),
        "community_cards_value_5": [-1] * len(data[0]['players_state'] * 4),
        "num_players": [],
        "own_stack": [],
        "own_cards_suit_0": [],
        "own_cards_value_0": [],
        "own_cards_suit_1": [],
        "own_cards_value_1": [],
        # "opponent_stacks": [],
        "actions": [],
        "amount": [],
    }

    rewards = {
        "round_rewards": [],
        "game_rewards": []
    }

    for round in data:
        for i, event in enumerate(round['events']):
            newData['rounds'].append(round['round'])
            newData['big_blind'].append(round['big_blind'])
            newData['small_blind'].append(round['small_blind'])
            newData['pot'].append(round['pot'])
            for i, card in enumerate(round['community_cards']):
                newData['community_cards_suit_{}'.format(i)].append(
                    suit_to_int[card['suit']])
                newData['community_cards_value_{}'.format(i)].append(
                    value_to_int[card['value']])
            newData['num_players'].append(len(round['players_state']))
            newData['own_stack'].append(round['players_state'][i]['stack'])
            for i, card in enumerate(round['players_state'][i]['cards']):
                newData['own_cards_suit_{}'.format(i)].append(
                    suit_to_int[card['suit']])
                newData['own_cards_value_{}'.format(i)].append(
                    value_to_int[card['value']])
            newData['actions'].append(action_to_int[event['action']])
            newData['amount'].append(event['amount'])
            rewards['round_rewards'].append(event['round_rewards'])
            rewards['game_rewards'].append(event['game_rewards'])

    print(newData['community_cards_suit_0'])

    return newData, rewards


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
    data, rewards = extract_all_actions(data)

    return data, rewards


def prepare_input(preprocessed_data: dict) -> torch.tensor:
    rounds = torch.tensor(preprocessed_data['rounds'], dtype=torch.float)
    big_blind = torch.tensor(preprocessed_data['big_blind'], dtype=torch.float)
    small_blind = torch.tensor(
        preprocessed_data['small_blind'], dtype=torch.float)
    pot = torch.tensor(preprocessed_data['pot'], dtype=torch.float)
    community_cards_suit_0 = torch.tensor(
        preprocessed_data['community_cards_suit_0'], dtype=torch.float)
    community_cards_value_0 = torch.tensor(
        preprocessed_data['community_cards_value_0'], dtype=torch.float)
    community_cards_suit_1 = torch.tensor(
        preprocessed_data['community_cards_suit_1'], dtype=torch.float)
    community_cards_value_1 = torch.tensor(
        preprocessed_data['community_cards_value_1'], dtype=torch.float)
    community_cards_suit_2 = torch.tensor(
        preprocessed_data['community_cards_suit_2'], dtype=torch.float)
    community_cards_value_2 = torch.tensor(
        preprocessed_data['community_cards_value_2'], dtype=torch.float)
    community_cards_suit_3 = torch.tensor(
        preprocessed_data['community_cards_suit_3'], dtype=torch.float)
    community_cards_value_3 = torch.tensor(
        preprocessed_data['community_cards_value_3'], dtype=torch.float)
    community_cards_suit_4 = torch.tensor(
        preprocessed_data['community_cards_suit_4'], dtype=torch.float)
    community_cards_value_4 = torch.tensor(
        preprocessed_data['community_cards_value_4'], dtype=torch.float)
    community_cards_suit_5 = torch.tensor(
        preprocessed_data['community_cards_suit_5'], dtype=torch.float)
    community_cards_value_5 = torch.tensor(
        preprocessed_data['community_cards_value_5'], dtype=torch.float)
    num_players = torch.tensor(
        preprocessed_data['num_players'], dtype=torch.float)
    own_stack = torch.tensor(preprocessed_data['own_stack'], dtype=torch.float)
    own_cards_suit_0 = torch.tensor(
        preprocessed_data['own_cards_suit_0'], dtype=torch.float)
    own_cards_value_0 = torch.tensor(
        preprocessed_data['own_cards_value_0'], dtype=torch.float)
    own_cards_suit_1 = torch.tensor(
        preprocessed_data['own_cards_suit_1'], dtype=torch.float)
    own_cards_value_1 = torch.tensor(
        preprocessed_data['own_cards_value_1'], dtype=torch.float)
    # opponent_stacks = torch.tensor(
    #     preprocessed_data['opponent_stacks'], dtype=torch.float)
    actions = torch.tensor(preprocessed_data['actions'], dtype=torch.float)
    amount = torch.tensor(preprocessed_data['amount'], dtype=torch.float)

    print(len(rounds))

    input_data = torch.stack((rounds, big_blind, small_blind, pot, community_cards_suit_0, community_cards_value_0, community_cards_suit_1, community_cards_value_1, community_cards_suit_2, community_cards_value_2, community_cards_suit_3,
                             community_cards_value_3, community_cards_suit_4, community_cards_value_4, community_cards_suit_5, community_cards_value_5, num_players, own_stack, own_cards_suit_0, own_cards_value_0, own_cards_suit_1, own_cards_value_1, actions, amount), dim=1)

    return input_data
