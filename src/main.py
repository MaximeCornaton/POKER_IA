from agent.cAgent import Agent
from environment.cPokerGame import PokerGame
from utils.config_loader import load_config


def main():
    num_episodes = 1

    game_config = load_config('configs/game_configs/texas_holdem.json')
    agent_config = load_config('configs/agent_configs/neural_network.json')

    # Création de l'agent
    agent = Agent(
        input_size=agent_config['input_size'],
        hidden_size=agent_config['hidden_size'],
        output_size=agent_config['output_size'],
        learning_rate=agent_config['learning_rate']
    )

    # Création de l'environnement
    environment = PokerGame(
        num_players=game_config['num_players'],
        starting_stack=game_config['starting_stack'],
        small_blind=game_config['small_blind'],
        big_blind=game_config['big_blind'],
        max_rounds=game_config['max_rounds']
    )

    # Boucle sur les épisodes
    for episode in range(num_episodes):

        environment.init_game(agent=agent)
        environment.play_game()

        # states, actions, rewards = environment.get_history()
        # agent.train(states, actions, rewards)


if __name__ == "__main__":
    main()
