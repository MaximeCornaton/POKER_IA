# Description: This file contains the class for a player in the game of poker.
# Author: Maxime Cornaton
# Date: 2023

from environment.ePlayerAction import PlayerAction


class Player:

    """
    _summary_ : Class used to create a player.
    _description_ : This class is used to create a player.
    _attributes_ :
        - agent : Agent used by the player.
        - name : Name of the player.
        - chips : Number of chips the player has.
        - hand : Hand of the player.
    _returns_ : None
    """

    def __init__(self, agent, name: str = "Player 1", chips: int = 1000) -> None:
        self.agent = agent

        self.name = name

        self.chips = chips
        self.hand = []

    """
    _summary_ : Make a decision.
    _description_ : This method is used to make a decision.
    _attributes_ :
        - env : Environment of the game.
        - min_bet : Minimum bet amount.
    _returns_ : None
    """

    def make_decision(self, env, min_bet: int) -> (PlayerAction, int):
        if self.chips == 0:
            return PlayerAction.FOLD, 0
        if self.chips < min_bet:
            return PlayerAction.ALL_IN, self.chips

        state = env.get_state()
        # return self.agent.make_decision(state)
        return PlayerAction.CHECK, 0

    """
    _summary_ :  Make a bet.
    _description_ : This method is used to make a bet.
    _attributes_ :
        - amount : Amount of the bet.
    _returns_ : None    
    """

    def bet(self, amount: int) -> None:
        self.chips -= amount

    def __str__(self) -> str:
        return f"{self.name}"
