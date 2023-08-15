import random


class Environment:
    def __init__(self, num_players, starting_stack, small_blind, big_blind, max_rounds):

        self.num_players = num_players
        self.starting_stack = starting_stack

        self.small_blind = small_blind
        self.big_blind = big_blind

        self.max_rounds = max_rounds

    def init_game(self):
        self.deck = self.generate_deck()
        self.players = self.generate_players()
        self.pot = 0
        self.community_cards = []

    def generate_players(self):
        return [Player(self.starting_stack) for _ in range(self.num_players)]

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

    def get_data(self):
        # Return the data to train the agent on
        pass

    def __str__(self):
        return f"Players: {self.players}\nPot: {self.pot}\nCommunity Cards: {self.community_cards}"


class Player:
    def __init__(self, chips):
        self.chips = chips
        self.hand = []

    def make_decision(self, env):
        # Replace this with your actual decision-making logic
        return 'bet', 10

    def bet(self, amount):
        self.chips -= amount


# Test the environment
if __name__ == '__main__':
    env = Environment(num_players=5)
    env.deal_cards()

    for player in env.players:
        print(f"Player's hand: {player.hand}")
