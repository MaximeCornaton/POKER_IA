from agent.cAgent import Agent
from environment.cPokerGame import PokerGame
from utils.config_manager import load_config
from utils.reward_manager import calculate_reward


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
        small_blind=game_config['small_blind'],
        big_blind=game_config['big_blind'],
        max_rounds=game_config['max_rounds']
    )

    for id in range(num_episodes):

        environment.init(agent=agent)
        winners = environment.play()

        environment.save_history(f"history_{id}.json")

        history = environment.get_history()

        data = calculate_reward(history, winners)

        # agent.train(states, actions, amounts)

        environment.reset()


if __name__ == "__main__":
    main()
