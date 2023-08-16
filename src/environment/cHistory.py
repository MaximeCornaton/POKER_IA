import json


class History:
    def __init__(self):
        self.reset()

    def reset(self):
        self.history = {
            'states': [],
            'player': [],
            'actions': [],
            'amounts': [],
        }

    def add(self, state, player, action, amount):
        self.history['states'].append(state)
        self.history['player'].append(player)
        self.history['actions'].append(action)
        self.history['amounts'].append(amount)

    def get(self):
        return self.history['states'], self.history['actions'], self.history['amounts']

    def get_players_and_amounts(self):
        return self.history['player'], self.history['amounts']

    def save(self, path):
        with open(path, 'w') as f:
            json.dump(self.history, f, indent=2)
