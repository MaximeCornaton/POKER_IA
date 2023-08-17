import torch
import numpy as np
# Assurez-vous que NeuralNetwork est correctement importé
from model.cModel import NeuralNetwork
import torch.optim as optim


class Agent:
    def __init__(self, input_size, hidden_size, output_size, learning_rate):
        self.model = NeuralNetwork(input_size, hidden_size, output_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)

    def train(self, data):
        # Entraînez le modèle avec les données fournies
        # Remplacez cette partie par votre propre logique d'entraînement
        pass
