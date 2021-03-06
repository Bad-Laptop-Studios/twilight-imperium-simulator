import sys
#from __future__ import *
from typing import *
sys.path.insert(0, 'D:/Documents/GitHub/twilight-imperium-simulator')
from players import *
from controller import log_warning

class StrategyCard():
    ID = None
    PRIMARY_TEXT: list[str] = None
    SECONDARY_TEXT: list[str] = None

    def __init__(self):
        self._id = self.ID
        self._name = self.__class__.__name__
        self._is_exhausted = False
        self._trade_goods = 0

    def get_name(self) -> str:
        return self._name

    def get_primary_text(self) -> List[str]:
        return self.PRIMARY_TEXT
    def get_secondary_text(self) -> List[str]:
        return self.SECONDARY_TEXT

    def resolve_primary(self):
        raise NotImplementedError
    def resolve_secondary(self):
        raise NotImplementedError

    def increment_trade_goods(self):
        self._trade_goods += 1

    def reset_trade_goods(self):
        self._trade_goods = 0

    def get_trade_goods(self):
        return self._trade_goods

    def exhaust(self) -> None:
        """ Exhaust strategy card. """
        self._is_exhausted = True

    def ready(self) -> None:
        """ Ready strategy card. """
        self._is_exhausted = False

    def _spend_strategy_token(self, player: Player, strategy_card: str) -> bool:
        """ Attempt to spend strategy token.
            Return whether or not it was successful. """
        if token_amount := player.command_tokens['strategy'] <= 0:
            log_warning(f"Player {player.get_id()} attempted to resolve the secondary of {strategy_card} with {token_amount} strategy tokens.")
            return False
        player.alter_command_tokens('strategy', -1)
        return True


class Leadership(StrategyCard):
    ID = 1
    PRIMARY_TEXT = ["Gain 3 command tokens.", "Spend any amount of influence to gain 1 command token for every 3 influence spent"]
    SECONDARY_TEXT = ["Spend any amount of influence to gain 1 command token for every 3 influence spent"]

    def resolve_primary(self, player: Player, influence_amount: int) -> None:
        player.alter_command_tokens(3) # method is not implemented yet
        self.resolve_secondary(player, influence_amount)

    def resolve_secondary(self, player: Player, influence_amount: int) -> None:
        """ Resolves the Secondary Ability for Leadership.
            Assumes influence_amount is non-negative.
            Note: the player will give the controller planets and the controller will give this method the influence sum. !!! delete this line after implementation"""
        token_amount = influence_amount // 3
        player.alter_commodities(token_amount)

class Diplomacy(StrategyCard):
    ID = 2
    PRIMARY_TEXT = ["Choose 1 system other than the Mecatol Rex system that contains a planet you control; each other player places a command token from their reinforcements in the chosen system. Then, ready up to 2 exhausted planets you control."]
    SECONDARY_TEXT = ["Spend 1 token from your strategy pool to ready up to 2 exhausted planets you control."]

    def resolve_primary(self):
        raise NotImplementedError

    def resolve_secondary(self):
        raise NotImplementedError
    
class Politics(StrategyCard):
    ID = 3
    PRIMARY_TEXT = ["Choose a player other than the speaker. That player gains the speaker token.", "Draw 2 action cards.", "Look at the top 2 cards of the agenda deck. Place each card on the top or bottom of the deck in any order"]
    SECONDARY_TEXT = ["Spend 1 token from your strategy pool to draw 2 action cards."]

    def resolve_primary(self, player_active: Player, player_chosen) -> None:
        # ability 1
        #something.set_speaker(player_chosen)
        # ability 2
        #player.draw_action_cards(2) # method does not exist yet. Alternately: something.draw_action_cards(player_active, 2)
        # ability 3
        raise NotImplementedError


    def resolve_secondary(self, player: Player) -> None:
        if token_amount := player.get_strategy_tokens() <= 0: # must remove the token too !!!
            log_warning(f"Player {player.get_id()} attempted to resolve the secondary of Politics with {token_amount} strategy tokens.")
        #player.draw_action_cards(2) # method does not exist yet. Alternately: something.draw_action_cards(player_active, 2)
        raise NotImplementedError
        
class Construction(StrategyCard):
    ID = 4
    PRIMARY_TEXT = ["Place 1 PDS or 1 Space Dock on a planet you control.", "Place 1 PDS on a planet you control."]
    SECONDARY_TEXT = ["Spend 1 token from your strategy pool and place it in any system; you may place either 1 space dock or 1 PDS on a planet you control in that system."]

    def resolve_primary(self):
        raise NotImplementedError

    def resolve_secondary(self):
        raise NotImplementedError
    
class Trade(StrategyCard):
    """ Trade strategy card. Handles card resolution. """
    ID = 4
    PRIMARY_TEXT = ["Gain 3 trade goods.", "Replenish commodities.", "Choose any number of other players. Those players use the secondary ability of this strategy card without spending a command token."]
    SECONDARY_TEXT = ["Spend 1 token from your strategy pool to replenish your commodities."]

    def __init__(self) -> None:
        super().__init__()
        self._allowed_free_secondary: list[Player] = []

    def resolve_primary(self, player: Player, player_list: list[Player]):
        player.alter_trade_goods(3)
        player.replenish_commodities()
        self._allowed_free_secondary = player_list

    def resolve_secondary(self, player: Player) -> None:
        if player in self.allowed_free_secondary:
            player.replenish_commodities()
        elif self._spend_strategy_token(player, self._name):
            player.replenish_commodities()

    def ready(self) -> None:
        super().ready()
        self._allowed_free_secondary = []

    @property
    def allowed_free_secondary(self) -> list[Player]:
        return self._allowed_free_secondary

    
class Warfare(StrategyCard):
    ID = 6
    PRIMARY_TEXT = ["Remove 1 of your command tokens from the game board; then, gain 1 command token.", "Redistribute any number of the command tokens on your command sheet"]
    SECONDARY_TEXT = ["Spend 1 token from your strategy pool to use the Production ability of 1 of your space docks in your home system."]

    def resolve_primary(self):
        raise NotImplementedError

    def resolve_secondary(self):
        raise NotImplementedError
    
class Technology(StrategyCard):
    ID = 7
    PRIMARY_TEXT = ["Research 1 technology.", "Spend 6 resources to research 1 technology."]
    SECONDARY_TEXT = ["Spend 1 token from your strategy pool and 4 resources to research 1 technology."]

    def resolve_primary(self):
        raise NotImplementedError

    def resolve_secondary(self):
        raise NotImplementedError
    
class Imperial(StrategyCard):
    ID = 8
    PRIMARY_TEXT = ["Immediately score 1 public objective if you fulfill its requirements.", "Gain 1 victory point if you control Mecatol Rex; otherwise, draw 1 secret objective"]
    SECONDARY_TEXT = ["Spend 1 token from your strategy pool to draw 1 secret objective."]

    def resolve_primary(self):
        raise NotImplementedError

    def resolve_secondary(self):
        raise NotImplementedError
    
