import json
import random


from environment.cPlayer import Player
from environment.cHandEvaluator import HandEvaluator
from environment.cHistory import History
from environment.ePlayerAction import PlayerAction


class PokerGame:
    def __init__(self, num_players, small_blind, big_blind, max_rounds):
        self.num_players = num_players

        self.small_blind = small_blind
        self.big_blind = big_blind

        self.max_rounds = max_rounds

    def init(self, agent):
        self.players = self.generate_players(agent)
        self.history = History()
        self.reset()

    def reset(self):
        self.pot = 0
        self.community_cards = []
        self.deck = self.generate_deck()
        self.reset_players_hands()
        self.history.reset()

    def reset_players_hands(self):
        for player in self.players:
            player.hand = []

    def generate_players(self, agent):
        return [Player(agent=agent) for _ in range(self.num_players)]

    def generate_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2', '3', '4', '5', '6', '7', '8',
                  '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        return [{'suit': suit, 'value': value} for suit in suits for value in values]

    def deal_cards(self):
        random.shuffle(self.deck)
        for player in self.players:
            player.hand = [self.deck.pop(), self.deck.pop()]

    def deal_community_cards(self, num_cards):
        for _ in range(num_cards):
            self.community_cards.append(self.deck.pop())

    def play_round(self, round_num):
        if round_num == self.max_rounds:
            return

        round_min_bet = 0

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

            self.history.add(state=self.get_state(), player=player,
                             action=decision, amount=amount)

        self.deal_community_cards(3 if round_num == 0 else 1)
        self.rotate_players()
        self.play_round(round_num + 1)

    def blind_bets(self):
        self.players[0].bet(self.small_blind)
        self.players[1].bet(self.big_blind)
        self.pot += self.small_blind + self.big_blind

    def rotate_players(self):
        self.players = self.players[1:] + self.players[:1]

    def play(self):
        self.deal_cards()
        self.play_round(0)

        winners = self.determine_winner()

        for winner in winners:
            winner.chips += self.pot / len(winners)

        self.history.save('data/history.json')

        self.reset()

    def calculate_rewards(self, winners):
        rewards = {
            'action_rewards': [],
            'game_rewards': [],
        }
        for player, amount in self.history.get_players_and_amounts():
            if player in winners:
                rewards['action_rewards'].append(amount)
                rewards['game_rewards'].append(amount)
            else:
                rewards['action_rewards'].append(-amount)
                rewards['game_rewards'].append(0)

    def determine_winner(self):
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

    def get_state(self):
        return {
            'player_hands': [player.hand for player in self.players],
            'community_cards': self.community_cards,
            'player_stacks': [player.chips for player in self.players],
            'pot': self.pot,
            'small_blind': self.small_blind,
            'big_blind': self.big_blind,
        }

    def __str__(self):
        return f"Players: {self.players}\nPot: {self.pot}\nCommunity Cards: {self.community_cards}"
