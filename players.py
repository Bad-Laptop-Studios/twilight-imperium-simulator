from typing import *

class Player:
    """
    Stores token pools, units, owned planets
    """
    def __init__(self, id: int):
        self.strategy_card = None
        self.faction = None
        self._fleet_tokens = 3
        self._tactic_tokens = 3
        self._strategy_tokens = 2
        self._commodities = 0
        
        self.planets = []
        self.ships = []

        self.activated_systems = []

        self.id = id
        self._unit_upgrades = []

    def select_strategy_card(self, card_number):
        self.strategy_card = card_number

    def deactivate_systems(self):
        """ Remove all activated systems. """
        self.activated_systems = []

    def get_id(self) -> int:
        return self.id

    def gain_command_tokens(self, amount: int) -> None:
        """ Increases the player's commodities by the amount.
        How do we implement this? How do we decide which pool to put the tokens in """
        raise NotImplementedError

    def change_commodities(self, amount: int) -> None:
        """ Changes the player's number of commodities by the amount. Ensures commodities remain non-negative. """
        self._commodities = max(0, self._commodities + amount)

    def draw_action_cards(self, number: int) -> None:
        """ Draws the number of action cards. Ensures player's action card count remains valid. """
        raise NotImplementedError

    def get_fleet_tokens(self) -> int:
        """ Returns the number of command tokens in the player's fleet pool. """
        return self._fleet_tokens
    def get_tactic_tokens(self) -> int:
        """ Returns the number of command tokens in the player's tactic pool. """
        return self._tactic_tokens
    def get_strategy_tokens(self) -> int:
        """ Returns the number of command tokens in the player's strategy pool. """
        return self._strategy_tokens

    def get_unit_upgrades(self) -> List[str]:
        """ Returns a list of all the units that are upgraded.
            Note that unlocking Warsuns is treated as an upgrade. """
        return self._unit_upgrades