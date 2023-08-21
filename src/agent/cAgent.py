import torch
import torch.optim as optim
from model.cModel import NeuralNetwork
from utils.preprocessing import prepare_input


class Agent:
    def __init__(self, input_size: int, hidden_size: int, output_size: int, learning_rate: float) -> None:
        self.model = NeuralNetwork(input_size, hidden_size, output_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)

    def train(self, data: dict, rewards: dict) -> None:

        output = self.model(prepare_input(data))

        round_rewards = torch.tensor(
            rewards['round_rewards'], dtype=torch.float)
        game_rewards = torch.tensor(
            rewards['game_rewards'], dtype=torch.float)

        loss = self.calculate_loss(output, round_rewards, game_rewards)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def prepare_input(self, preprocessed_data: dict) -> torch.tensor:
        input_data = preprocessed_data

        return input_data

    def calculate_loss(self, output: torch.tensor, round_rewards: torch.tensor, game_rewards: torch.tensor) -> torch.tensor:
        # Calculez la perte entre les prédictions du modèle et les récompenses réelles
        loss = torch.mean((output - round_rewards) ** 2 +
                          (output - game_rewards) ** 2)
        return loss
