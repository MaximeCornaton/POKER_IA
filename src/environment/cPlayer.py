class Player:
    def __init__(self, agent, chips=1000):
        self.agent = agent

        self.chips = chips
        self.hand = []

    def make_decision(self, env):
        state = env.get_state()
        # return self.agent.make_decision(state)
        return "bet", 10

    def bet(self, amount):
        self.chips -= amount

    def __str__(self):
        return f"Chips: {self.chips}\nHand: {self.hand}"
