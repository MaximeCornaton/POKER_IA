import json


class History:
    def __init__(self):
        self.reset()

    def reset(self):
        self.history = {
            'states': [],
            'actions': [],
            'rewards': []
        }

    def add(self, state, action, reward):
        self.history['states'].append(state)
        self.history['actions'].append(action)
        self.history['rewards'].append(reward)

    def update_rewards(self, rewards):
        self.history['rewards'] = rewards

    def get(self):
        return self.history['states'], self.history['actions'], self.history['rewards']

    def save(self, path):
        with open(path, 'w') as f:
            json.dump(self.history, f, indent=2)
