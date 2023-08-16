class HandEvaluator:
    def __init__(self):
        self.hand_rankings = {
            "High Card": 0,
            "One Pair": 1,
            "Two Pairs": 2,
            "Three of a Kind": 3,
            "Straight": 4,
            "Flush": 5,
            "Full House": 6,
            "Four of a Kind": 7,
            "Straight Flush": 8,
            "Royal Flush": 9
        }

    def evaluate_hand(self, hand, community_cards):
        all_cards = hand + community_cards
        all_cards.sort(key=lambda card: card['value'])

        for method_name in self.hand_rankings:
            method = getattr(
                self, f'is_{method_name.lower().replace(" ", "_")}', None)
            if method and method(all_cards):
                return self.hand_rankings[method_name]

        return self.hand_rankings["High Card"]

    def is_royal_flush(self, cards):
        return self.is_straight_flush(cards) and self.has_ace_high(cards)

    def is_straight_flush(self, cards):
        return self.is_straight(cards) and self.is_flush(cards)

    def is_four_of_a_kind(self, cards):
        value_counts = self.get_value_counts(cards)
        return any(count >= 4 for count in value_counts.values())

    def is_full_house(self, cards):
        value_counts = self.get_value_counts(cards)
        return any(count >= 3 for count in value_counts.values()) and len(value_counts) == 2

    def is_flush(self, cards):
        return all(card['suit'] == cards[0]['suit'] for card in cards)

    def is_straight(self, cards):
        value_counts = self.get_value_counts(cards)
        if len(value_counts) < 5:
            return False

        values = sorted(set(card['value'] for card in cards))
        for i in range(len(values) - 4):
            if values[i] == values[i + 4]:
                return True
        return False

    def is_three_of_a_kind(self, cards):
        value_counts = self.get_value_counts(cards)
        return any(count >= 3 for count in value_counts.values())

    def is_two_pairs(self, cards):
        value_counts = self.get_value_counts(cards)
        pairs = [value for value, count in value_counts.items() if count >= 2]
        return len(pairs) >= 2

    def is_one_pair(self, cards):
        value_counts = self.get_value_counts(cards)
        return any(count >= 2 for count in value_counts.values())

    def get_value_counts(self, cards):
        value_counts = {}
        for card in cards:
            value = card['value']
            value_counts[value] = value_counts.get(value, 0) + 1
        return value_counts

    def has_ace_high(self, cards):
        return any(card['value'] == 'Ace' for card in cards)

    def tiebreaker_rank(self, hand, community_cards):
        all_cards = hand + community_cards
        all_cards.sort(key=lambda card: card['value'], reverse=True)


if __name__ == "__main__":
    hand_evaluator = HandEvaluator()
    hand = [{'suit': 'Hearts', 'value': '6'}, {'suit': 'Clubs', 'value': '6'}]
    community_cards = [{'suit': 'Diamonds', 'value': '2'}, {
        'suit': 'Spades', 'value': '8'}, {'suit': 'Clubs', 'value': '10'}]
    hand_strength = hand_evaluator.evaluate_hand(hand, community_cards)
    print("Hand strength:", hand_strength)
