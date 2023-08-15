class HandEvaluator:
    def __init__(self):
        self.hand_rankings = {
            "High Card": 0,
            "One Pair": 1,
            "Two Pairs": 2,
            # ... Ajoutez d'autres combinaisons de mains et scores ici
        }

    def evaluate_hand(self, hand, community_cards):
        all_cards = hand + community_cards
        all_cards.sort(key=lambda card: card['value'])

        # Vérification pour une paire
        for i in range(len(all_cards) - 1):
            if all_cards[i]['value'] == all_cards[i + 1]['value']:
                return self.hand_rankings["One Pair"]

        # Vérification pour deux paires
        pair_count = 0
        for i in range(len(all_cards) - 1):
            if all_cards[i]['value'] == all_cards[i + 1]['value']:
                pair_count += 1
                if pair_count == 2:
                    return self.hand_rankings["Two Pairs"]

        return self.hand_rankings["High Card"]


# Test
hand_evaluator = HandEvaluator()
hand = [{'suit': 'Hearts', 'value': '6'}, {'suit': 'Clubs', 'value': '6'}]
community_cards = [{'suit': 'Diamonds', 'value': '2'}, {
    'suit': 'Spades', 'value': '8'}, {'suit': 'Clubs', 'value': '10'}]
hand_strength = hand_evaluator.evaluate_hand(hand, community_cards)
print("Hand strength:", hand_strength)
