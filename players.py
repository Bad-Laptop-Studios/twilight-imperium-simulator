from typing import *

CommandPool = Literal['fleet', 'tactic', 'strategy']
CommandSheet = dict[CommandPool, int]
""" Dictionary of the 3 command pools. """


class Player:
    """
    Stores token pools, units, owned planets
    """
    def __init__(self, id: int):
        self.strategy_card = None
        self.faction = None
        self._command_tokens = {'fleet': 3, 'tactic': 3, 'strategy': 2}
        self._commodities = 0
        self._commodity_bonus = 0
        self._trade_goods = 0
        
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


    # ---------- Command Tokens ---------- #
    @property
    def command_tokens(self) -> CommandSheet:
        """ Return command tokens in each pool. """
        return self._command_tokens
    def get_command_tokens(self, pool: str) -> int:
        """ Return number of command tokens in command pool.
            Assumes pool is in ['fleet', 'tactic', 'strategy']. """
        return self._command_tokens[pool]
    def alter_command_tokens(self, pool: str, amount: int) -> None:
        """ Alter command pool value by amount.
            Assumes pool is in ['fleet', 'tactic', 'strategy']. """
        self._command_tokens[pool] += amount

    # ---------- Commodities ---------- #
    @property
    def commodities(self) -> int:
        """ Return number of commodities. """
        return self._commodities
    def alter_commodities(self, amount: int) -> None:
        """ Change the player's number of commodities by the amount. Ensures commodities remain non-negative. """
        self._commodities = max(0, self._commodities + amount)
    def replenish_commodities(self) -> None:
        """ Replenish commodities. """
        self._commodities = self._faction.commodities + self._commodity_bonus

    # ---------- Action Cards ---------- #
    def draw_action_cards(self, number: int) -> None:
        """ Draw the number of action cards. Ensures player's action card count remains valid. """
        raise NotImplementedError

    # ---------- Units ---------- #
    def get_unit_upgrades(self) -> List[str]:
        """ Return a list of all the units that are upgraded.
            Note that unlocking Warsuns is treated as an upgrade. """
        return self._unit_upgrades

    # ---------- Trade Goods ---------- #
    @property
    def trade_goods(self) -> None:
        return self._trade_goods
    @trade_goods.setter
    def trade_goods(self, value: int) -> None:
        """ Set the player's number of trade goods to the value. """
        self._trade_goods = value
    def alter_trade_goods(self, amount: int) -> bool:
        """ Add amount to player's trade goods. Returns False if final value is maxed to 0, True otherwise."""
        value = self.trade_goods + amount
        self.trade_goods = max(0, value)
        return value >= 0

