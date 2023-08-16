import json


class History:
    def __init__(self):
        self.reset()

    def reset(self):
        self.history = {
            'states': [],
            'players': [],
            'actions': [],
            'amounts': [],
        }

    def add(self, state, player, action, amount):
        self.history['states'].append(state)
        self.history['players'].append(player)
        self.history['actions'].append(action)
        self.history['amounts'].append(amount)

    def get(self):
        return self.history['states'], self.history['actions'], self.history['amounts']

    def get_players_and_amounts(self):
        return self.history['players'], self.history['amounts']

    def save(self, path):
        history = {
            'states': self.history['states'],
            'player': [str(player) for player in self.history['players']],
            'actions': [action.name for action in self.history['actions']],
            'amounts': self.history['amounts'],
        }

        with open(path, 'w') as f:
            json.dump(history, f, indent=2)
