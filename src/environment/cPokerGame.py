import json
import random

from environment.cHandEvaluator import HandEvaluator


class Environment:
    def __init__(self, num_players, starting_stack, small_blind, big_blind, max_rounds):

        self.num_players = num_players
        self.starting_stack = starting_stack

        self.small_blind = small_blind
        self.big_blind = big_blind

        self.max_rounds = max_rounds

    def init_game(self, agent):
        self.history = {'states': [], 'actions': [], 'rewards': []}
        self.deck = self.generate_deck()
        self.players = self.generate_players(agent)
        self.pot = 0
        self.community_cards = []

    def generate_players(self, agent):
        return [Player(agent=agent, chips=self.starting_stack) for _ in range(self.num_players)]

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

        for player in self.players:

            decision, amount = player.make_decision(self)
            if decision == 'fold':
                continue
            if decision == 'bet':
                player.bet(amount)
                self.pot += amount

        self.deal_community_cards(3 if round_num == 0 else 1)
        self.play_round(round_num + 1)

    def play_game(self):
        self.deal_cards()
        self.play_round(0)

        winner = self.determine_winner()
        for player in self.players:
            if player == winner:
                reward = 1.0
            else:
                reward = -1.0
            player.reward = reward

    def determine_winner(self):
        hand_evaluator = HandEvaluator()
        best_hand_strength = -1
        winning_player_index = -1

        for i, player in enumerate(self.players):
            hand_strength = hand_evaluator.evaluate_hand(
                player.hand, self.community_cards)

            if hand_strength > best_hand_strength:
                best_hand_strength = hand_strength
                winning_player_index = i

        return winning_player_index

    def get_state(self):
        return {
            'player_hands': [player.hand for player in self.players],
            'community_cards': self.community_cards,
            'player_stacks': [player.chips for player in self.players],
            # 'current_player_index': self.current_player_index,
            'pot': self.pot,
            # 'current_bets': [player.current_bet for player in self.players],
            'small_blind': self.small_blind,
            'big_blind': self.big_blind,
        }

    def get_history(self):
        return self.history['states'], self.history['actions'], self.history['rewards']

    def add_to_history(self, state, action, reward):
        self.history['states'].append(state)
        self.history['actions'].append(action)
        self.history['rewards'].append(reward)

    def save_history(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.history, f)

    def __str__(self):
        return f"Players: {self.players}\nPot: {self.pot}\nCommunity Cards: {self.community_cards}"


class Player:
    def __init__(self, agent, chips):
        self.agent = agent

        self.chips = chips
        self.hand = []

    def make_decision(self, env):
        state = env.get_state()
        return self.agent.make_decision(state)

    def bet(self, amount):
        self.chips -= amount

    def __str__(self):
        return f"Chips: {self.chips}\nHand: {self.hand}"
