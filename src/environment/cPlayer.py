from environment.ePlayerAction import PlayerAction


class Player:
    def __init__(self, agent, chips=1000):
        self.agent = agent

        self.chips = chips
        self.hand = []

    def make_decision(self, env, min_bet):
        if self.chips == 0:
            return PlayerAction.FOLD, 0
        if self.chips < min_bet:
            return PlayerAction.ALL_IN, self.chips

        state = env.get_state()
        # return self.agent.make_decision(state)
        return PlayerAction.CHECK, 0

    def bet(self, amount):
        self.chips -= amount

    def __str__(self):
        return f"Chips: {self.chips}\nHand: {self.hand}"
