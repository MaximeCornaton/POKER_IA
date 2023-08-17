# Description: This file contains the class HandEvaluator which is used to evaluate the strength of a hand.
# Author: Maxime Cornaton
# Date: 2023

class HandEvaluator:

    """
    _summary_ : Class used to evaluate the strength of a hand.
    _description_ : This class is used to evaluate the strength of a hand.
    _attributes_ :
        - hand_rankings : Dictionary containing the different hand rankings.
    _returns_ : None
    """

    def __init__(self) -> None:
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

    """
    _summary_ : Evaluate the strength of a hand.
    _description_ : This method is used to evaluate the strength of a hand.
    _attributes_ :
        - hand : Hand of the player.    
        - community_cards : Community cards.
    _returns_ : Strength of the hand.
    """

    def evaluate_hand(self, hand: list, community_cards: list) -> int:
        all_cards = hand + community_cards
        all_cards.sort(key=lambda card: self.card_value_key(card['value']))

        for method_name in self.hand_rankings:
            method = getattr(
                self, f'is_{method_name.lower().replace(" ", "_")}', None)
            if method and method(all_cards):
                return self.hand_rankings[method_name]

        return self.hand_rankings["High Card"]

    """
    _summary_ : Evaluate the strength of a hand.
    _description_ : This method is used to evaluate the strength of a hand.
    _attributes_ :
        - hand : Hand of the player.
        - community_cards : Community cards.
    _returns_ : Strength of the hand.
    """

    def tiebreaker_rank(self, hand: list, community_cards: list) -> int:
        all_cards = hand + community_cards
        all_cards.sort(key=lambda card: self.card_value_key(card['value']))

        value_counts = self.get_value_counts(all_cards)
        sorted_values = sorted(value_counts.keys(), key=lambda value: (
            value_counts[value], self.card_value_key(value)), reverse=True)

        tiebreaker_rank = 0
        for value in sorted_values:
            tiebreaker_rank = tiebreaker_rank * 13 + self.card_value_key(value)

        return tiebreaker_rank

    """
    _summary_ : Get the key of a card value.
    _description_ : This method is used to get the key of a card value.
    _attributes_ :
        - value : Value of the card.
    _returns_ : Key of the card value.
    """

    def card_value_key(self, value: str) -> int:
        # Define the custom order of card values
        value_order = ["2", "3", "4", "5", "6", "7", "8",
                       "9", "10", "Jack", "Queen", "King", "Ace"]
        return value_order.index(value)

    """
    _summary_ : Check if the hand is a royal flush.
    _description_ : This method is used to check if the hand is a royal flush.
    _attributes_ :
        - cards : Cards of the player.
    _returns_ : True if the hand is a royal flush, False otherwise.
    """

    def is_royal_flush(self, cards: list) -> bool:
        return self.is_straight_flush(cards) and self.has_ace_high(cards)

    """
    _summary_ : Check if the hand is a straight flush.
    _description_ : This method is used to check if the hand is a straight flush.
    _attributes_ :
        - cards : Cards of the player.
    _returns_ : True if the hand is a straight flush, False otherwise.
    """

    def is_straight_flush(self, cards: list) -> bool:
        return self.is_straight(cards) and self.is_flush(cards)

    """
    _summary_ : Check if the hand is a four of a kind.
    _description_ : This method is used to check if the hand is a four of a kind.
    _attributes_ :
        - cards : Cards of the player.
    _returns_ : True if the hand is a four of a kind, False otherwise.
    """

    def is_four_of_a_kind(self, cards: list) -> bool:
        value_counts = self.get_value_counts(cards)
        return any(count >= 4 for count in value_counts.values())

    """
    _summary_ : Check if the hand is a full house.
    _description_ : This method is used to check if the hand is a full house.
    _attributes_ :
        - cards : Cards of the player.
    _returns_ : True if the hand is a full house, False otherwise.
    """

    def is_full_house(self, cards: list) -> bool:
        value_counts = self.get_value_counts(cards)
        return any(count >= 3 for count in value_counts.values()) and len(value_counts) == 2

    """
    _summary_ : Check if the hand is a flush.
    _description_ : This method is used to check if the hand is a flush.
    _attributes_ :
        - cards : Cards of the player.
    _returns_ : True if the hand is a flush, False otherwise.
    """

    def is_flush(self, cards: list) -> bool:
        return all(card['suit'] == cards[0]['suit'] for card in cards)

    """
    _summary_ : Check if the hand is a straight.    
    _description_ : This method is used to check if the hand is a straight.
    _attributes_ :
        - cards : Cards of the player.  
    _returns_ : True if the hand is a straight, False otherwise.
    """

    def is_straight(self, cards: list) -> bool:
        value_counts = self.get_value_counts(cards)
        if len(value_counts) < 5:
            return False

        values = sorted(set(card['value'] for card in cards))
        # Check for regular straight
        for i in range(len(values) - 4):
            if values[i] == values[i + 4]:
                return True
        # Check for A-2-3-4-5 straight
        if 'Ace' in values and '2' in values and '3' in values and '4' in values and '5' in values:
            return True
        return False

    """
    _summary_ : Check if the hand is a three of a kind.
    _description_ : This method is used to check if the hand is a three of a kind.
    _attributes_ :
        - cards : Cards of the player.
    _returns_ : True if the hand is a three of a kind, False otherwise.
    """

    def is_three_of_a_kind(self, cards: list) -> bool:
        value_counts = self.get_value_counts(cards)
        return any(count >= 3 for count in value_counts.values())

    """
    _summary_ : Check if the hand is two pairs.
    _description_ : This method is used to check if the hand is two pairs.
    _attributes_ :
        - cards : Cards of the player.
    _returns_ : True if the hand is two pairs, False otherwise.
    """

    def is_two_pairs(self, cards: list) -> bool:
        value_counts = self.get_value_counts(cards)
        pairs = [value for value, count in value_counts.items() if count >= 2]
        return len(pairs) >= 2

    """
    _summary_ : Check if the hand is one pair.
    _description_ : This method is used to check if the hand is one pair.
    _attributes_ :
        - cards : Cards of the player.
    _returns_ : True if the hand is one pair, False otherwise.
    """

    def is_one_pair(self, cards: list) -> bool:
        value_counts = self.get_value_counts(cards)
        return any(count >= 2 for count in value_counts.values())

    """ 
    _summary_ : Get the value counts.
    _description_ : This method is used to get the value counts.
    _attributes_ :
        - cards : Cards of the player.  
    _returns_ : Value counts.
    """

    def get_value_counts(self, cards: list) -> dict:
        value_counts = {}
        for card in cards:
            value = card['value']
            value_counts[value] = value_counts.get(value, 0) + 1
        return value_counts

    """
    _summary_ : Check if the hand has an ace high.
    _description_ : This method is used to check if the hand has an ace high.
    _attributes_ :
        - cards : Cards of the player.
    _returns_ : True if the hand has an ace high, False otherwise.
    """

    def has_ace_high(self, cards: list) -> bool:
        return any(card['value'] == 'Ace' for card in cards)


if __name__ == "__main__":
    hand_evaluator = HandEvaluator()
    hand = [{'suit': 'Hearts', 'value': '6'}, {'suit': 'Clubs', 'value': '6'}]
    community_cards = [{'suit': 'Diamonds', 'value': '2'}, {
        'suit': 'Spades', 'value': '8'}, {'suit': 'Clubs', 'value': '10'}]
    hand_strength = hand_evaluator.evaluate_hand(hand, community_cards)
    print("Hand strength:", hand_strength)
