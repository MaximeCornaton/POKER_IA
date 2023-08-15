import torch
import numpy as np
from model.model import NeuralNetwork
import torch.optim as optim


class Agent:
    def __init__(self, input_size, hidden_size, output_size, learning_rate):
        self.model = NeuralNetwork(input_size, hidden_size, output_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)

    def preprocess_state(self, game_state):
        # Preprocess the game state to a format suitable for the model
        return np.array([...])

    def make_decision(self, game_state):
        state = self.preprocess_state(game_state)
        input_data = torch.tensor(state, dtype=torch.float32)
        output = self.model(input_data)

        # Process the output to decide on an action
        decision, amount = self.process_output(output)
        return decision, amount

    def process_output(self, output):
        # Process the model's output to decide on an action
        probabilities = torch.softmax(output, dim=-1)
        action = torch.argmax(probabilities)
        return action.item()  # Return the action as an integer

    def train(self, states, actions, rewards):
        # Train the model using the collected states, actions, and rewards
        states_tensor = torch.tensor(states, dtype=torch.float32)
        actions_tensor = torch.tensor(actions, dtype=torch.int64)
        rewards_tensor = torch.tensor(rewards, dtype=torch.float32)

        self.optimizer.zero_grad()
        output = self.model(states_tensor)
        action_log_probs = torch.log_softmax(output, dim=-1)
        selected_action_log_probs = torch.gather(
            action_log_probs, 1, actions_tensor.unsqueeze(1))
        loss = -selected_action_log_probs.mean() * rewards_tensor
        loss.backward()
        self.optimizer.step()
