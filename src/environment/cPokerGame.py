# Description: This file contains the PokerGame class.
# Author: Maxime Cornaton
# Date: 2023

import random

from environment.cPlayer import Player
from environment.cHandEvaluator import HandEvaluator
from environment.cHistory import History
from environment.ePlayerAction import PlayerAction


class PokerGame:
    """
    _summary_ : Class used to create a poker game.
    _description_ : This class is used to create a poker game.
    _attributes_ :  
        - num_players : Number of players in the game.
        - small_blind : Small blind amount.
        - big_blind : Big blind amount.
        - max_rounds : Maximum number of rounds.
    _returns_ : None
    """

    def __init__(self, num_players: int, small_blind: int, big_blind: int, max_rounds: int) -> None:
        self.num_players = num_players

        self.small_blind = small_blind
        self.big_blind = big_blind

        self.max_rounds = max_rounds

    """
    _summary_ : Initialize the game.
    _description_ : This method is used to initialize the game.
    _attributes_ :
        - agent : Agent used to play the game.
    _returns_ : None
    """

    def init(self, agent: object) -> None:
        self.players = self.generate_players(agent)
        self.history = History()
        self.reset()

    """
    _summary_ : Reset the game.
    _description_ : This method is used to reset the game.
    _attributes_ : None
    _returns_ : None
    """

    def reset(self) -> None:
        self.pot = 0
        self.community_cards = []
        self.deck = self.generate_deck()
        self.reset_players_hands()
        self.history.reset()

    """
    _summary_ : Reset the players' hands.
    _description_ : This method is used to reset the players' hands.
    _attributes_ : None
    _returns_ : None    
    """

    def reset_players_hands(self) -> None:
        for player in self.players:
            player.hand = []

    """
    _summary_ : Generate the players.
    _description_ : This method is used to generate the players.
    _attributes_ :
        - agent : Agent used to play the game. 
    _returns_ : List of players 
    """

    def generate_players(self, agent: object) -> list:
        return [Player(agent=agent, name="Player_"+str(_)) for _ in range(self.num_players)]

    """
    _summary_ : Generate the deck.
    _description_ : This method is used to generate the deck.
    _attributes_ : None
    _returns_ : List of cards
    """

    def generate_deck(self) -> list:
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2', '3', '4', '5', '6', '7', '8',
                  '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        return [{'suit': suit, 'value': value} for suit in suits for value in values]

    """
    _summary_ : Deal the cards.
    _description_ : This method is used to deal the cards.
    _attributes_ : None
    _returns_ : None
    """

    def deal_cards(self) -> None:
        random.shuffle(self.deck)
        for player in self.players:
            player.hand = [self.deck.pop(), self.deck.pop()]

    """
    _summary_ : Deal the community cards.
    _description_ : This method is used to deal the community cards.
    _attributes_ :
        - num_cards : Number of cards to deal.
    _returns_ : None
    """

    def deal_community_cards(self, num_cards: int) -> None:
        for _ in range(num_cards):
            self.community_cards.append(self.deck.pop())

    """
    _summary_ : Play a round.
    _description_ : This method is used to play a round.
    _attributes_ :
        - round_num : Round number. 
    _returns_ : None
    """

    def play_round(self, round_num: int) -> None:
        if round_num == self.max_rounds:
            return

        round_min_bet = 0
        state = self.get_state()
        events = []

        if round_num == 0:
            self.blind_bets()

        for i, player in enumerate(self.players):

            player_min_bet = self.small_blind if i == 0 and round_num == 0 else self.big_blind if i == 1 and round_num == 0 else round_min_bet

            decision, amount = player.make_decision(
                env=self, min_bet=player_min_bet)

            if decision in [PlayerAction.CALL, PlayerAction.BET, PlayerAction.RAISE, PlayerAction.ALL_IN]:
                player.bet(amount)
                self.pot += amount

            round_min_bet = max(round_min_bet, amount)

            events.append({
                'player': player,
                'action': decision,
                'amount': amount
            })

        self.history.add(round_num, state, events)

        self.deal_community_cards(3 if round_num == 0 else 1)
        self.rotate_players()
        self.play_round(round_num + 1)

    """
    _summary_ : Make the blind bets.
    _description_ : This method is used to make the blind bets.
    _attributes_ : None
    _returns_ : None
    """

    def blind_bets(self) -> None:
        self.players[0].bet(self.small_blind)
        self.players[1].bet(self.big_blind)
        self.pot += self.small_blind + self.big_blind

    """
    _summary_ : Rotate the players.
    _description_ : This method is used to rotate the players.
    _attributes_ : None
    _returns_ : None
    """

    def rotate_players(self) -> None:
        self.players = self.players[1:] + self.players[:1]

    """
    _summary_ : Play the game.
    _description_ : This method is used to play the game.
    _attributes_ : None
    _returns_ : List of winners
    """

    def play(self) -> list:
        self.deal_cards()
        self.play_round(0)

        winners = self.determine_winner()

        for winner in winners:
            winner.chips += self.pot / len(winners)

        return winners

    """
    _summary_ : Save the history.
    _description_ : This method is used to save the history.
    _attributes_ :
        - path : Path to save the history.
    _returns_ : None
    """

    def save_history(self, path: str) -> None:
        self.history.save(path)

    """
    _summary_ : Determine the winner.
    _description_ : This method is used to determine the winner.
    _attributes_ : None
    _returns_ : List of winners
    """

    def determine_winner(self) -> list:
        hand_evaluator = HandEvaluator()
        best_hand_strength = -1
        winning_players = []

        for player in self.players:
            hand_strength = hand_evaluator.evaluate_hand(
                player.hand, self.community_cards)

            if hand_strength > best_hand_strength:
                best_hand_strength = hand_strength
                winning_players = [player]
            elif hand_strength == best_hand_strength:
                tiebreaker_rank = hand_evaluator.tiebreaker_rank(
                    player.hand, self.community_cards)
                winning_tiebreaker_rank = hand_evaluator.tiebreaker_rank(
                    winning_players[0].hand, self.community_cards)
                if tiebreaker_rank > winning_tiebreaker_rank:
                    winning_players = [player]
                elif tiebreaker_rank == winning_tiebreaker_rank:
                    winning_players.append(player)

        return winning_players

    """
    _summary_ : Get the state.
    _description_ : This method is used to get the state.
    _attributes_ : None
    _returns_ : State
    """

    def get_state(self) -> dict:
        return {
            'big_blind': self.big_blind,
            'small_blind': self.small_blind,
            'pot': self.pot,
            'community_cards': self.community_cards,
            'players_state': self.get_players_state(),
        }

    def get_players_state(self) -> list:
        return [{
            'player': player,
            'stack': player.chips,
            'cards': player.hand
        } for player in self.players]

    def __str__(self) -> str:
        return f"Players: {self.players}\nPot: {self.pot}\nCommunity Cards: {self.community_cards}"
