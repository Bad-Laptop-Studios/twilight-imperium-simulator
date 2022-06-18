from typing import *

from Manager import Player

class StrategyCard():
    def __init__(self):
        self._name = __name__
        self._is_exhausted = False
        self._primary_text = None
        self._secondary_text = None

    def get_primary_text(self) -> List[str]:
        return self._primary_text

    def get_secondary_text(self) -> List[str]:
        return self._secondary_text

    def resolve_primary(self):
        raise NotImplementedError

    def resolve_secondary(self):
        raise NotImplementedError

class Leadership(StrategyCard):
    def __init__(self):
        self._primary_text = ["Gain 3 command tokens.", "Spend any amount of influence to gain 1 command token for every 3 influence spent"]
        self._primary_code = "" # custom programming language to represent above
        self._secondary_text = ["Spend any amount of influence to gain 1 command token for every 3 influence spent"]
        self._secondary_code = "" # custom programming language to represent above

    def resolve_primary(self, player: Player) -> None:
        player.change_commodities(3) # method does not exist yet
        self.resolve_secondary(player)

    def resolve_secondary(self, player: Player) -> None:
        # the following is NOT actual Python code
        # the ability depends on implementation of the calling class
        value = "however this INTEGER is calculated"
        player.change_command_tokens(value)

class Diplomacy(StrategyCard):
    def __init__(self):
        pass

    def resolve_primary(self):
        raise NotImplementedError

    def resolve_secondary(self):
        raise NotImplementedError
    
class Politics(StrategyCard):
    def __init__(self):
        self._primary_text = ["Choose a player other than the speaker. That player gains the speaker token.", "Draw 2 action cards.", "Look at the top 2 cards of the agenda deck. Place each card on the top or bottom of the deck in any order"]
        self._primary_code = "" # custom programming language to represent above
        self._secondary_text = ["Spend 1 token from your strategy pool to draw 2 action cards."]
        self._secondary_code = "" # custom programming language to represent above

    def resolve_primary(self, player: Player) -> None:
        # ability 1
        # ability 2
        player.draw_action_cards(2) # method does not exist yet
        # ability 3

    def resolve_secondary(self, player: Player) -> None:
        pass

class Construction(StrategyCard):
    def __init__(self):
        pass

    def resolve_primary(self):
        raise NotImplementedError

    def resolve_secondary(self):
        raise NotImplementedError
    
class Trade(StrategyCard):
    def __init__(self):
        pass

    def resolve_primary(self):
        raise NotImplementedError

    def resolve_secondary(self):
        raise NotImplementedError
    
class Warfare(StrategyCard):
    def __init__(self):
        pass

    def resolve_primary(self):
        raise NotImplementedError

    def resolve_secondary(self):
        raise NotImplementedError
    
class Technology(StrategyCard):
    def __init__(self):
        pass

    def resolve_primary(self):
        raise NotImplementedError

    def resolve_secondary(self):
        raise NotImplementedError
    
class Imperial(StrategyCard):
    def __init__(self):
        pass

    def resolve_primary(self):
        raise NotImplementedError

    def resolve_secondary(self):
        raise NotImplementedError
    