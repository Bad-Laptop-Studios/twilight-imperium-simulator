import constants
from players import *

# The backets is the modifier. x for multiply, + for addition.
Stats = tuple[int, int, int, int]
"""cost (x), combat (x), move (+), capacity (+)"""

Abilities = tuple[int, int, int, int, int, int]
"""anit-fighter barrage (x), bombardement (x), planetary shield (?), production (+), space cannon (x), sustain damage (?)"""

TechnologyColour = Literal['green', 'red', 'blue', 'yellow']
TechnologyPrerequisites = dict[TechnologyColour, int]

class Unit:
    STATS_BASE: Stats      = 0, 0, 0, 0
    STATS_UPGRADED: Stats  = 0, 0, 0, 0
    STATS_MODIFIERS: Stats = 1, 1, 0, 0
    ABILITIES_BASE: Abilities               = 0, 0, 0, 0, 0, 0
    ABILITIES_MODIFIERS_BASE: Abilities     = 1, 1, 0, 0, 1, 0
    ABILITIES_UPGRADED: Abilities           = 0, 0, 0, 0, 0, 0
    ABILITIES_MODIFIERS_UPGRADED: Abilities = 1, 1, 0, 0, 1, 0
    ABILITY_CODE_BASE = ""      # for mechs
    ABILITY_CODE_UPGRADE = ""   # for Infantry II
    UPGRADE_PREREQUISITES: TechnologyPrerequisites = dict()

    def __init__(self, player: Player):
        # unit status
        self._is_sustained = False #: test
        self._player = None

        self._type = ""
        self._carrying = []
        self._check_for_faction_specific_units(player)

    def _check_for_faction_specific_units(player: Player) -> None:
        """ If the player's faction has specific units, use them instead. """
        pass

    def has_sustained(self) -> bool:
        """ Returns whether or not the unit has sustained damage. """
        return self._is_sustained

    def get_stats(self) -> tuple:
        """ Returns the full unit stats.
            
        Returns:
            cost: int
            combat: int
            move: int
            capacity: int
            cost_units: int (how many units you can produce for the one cost)
            combat_burst: int
        """
        return self._stats + self._cost_units + self._combat_burst


# ---------- SHIPS ---------- #
class Ship(Unit):
    pass


class Carrier(Ship):
    STATS_BASE: Stats     = 3, 9, 1, 4
    STATS_UPGRADED: Stats = 3, 9, 2, 6
    UPGRADE_PREREQUISITES: TechnologyPrerequisites = {'blue':2}


class Cruiser(Ship):
    STATS_BASE: Stats     = 2, 7, 2, 0
    STATS_UPGRADED: Stats = 2, 6, 3, 1
    UPGRADE_PREREQUISITES: TechnologyPrerequisites = {'green':1, 'yellow':1, 'red':1}


class Destroyer(Ship):
    STATS_BASE: Stats     = 1, 9, 2, 0
    STATS_UPGRADED: Stats = 1, 8, 2, 0
    ABILITIES_BASE: Abilities               = 9, 0, 0, 0, 0, 0
    ABILITIES_MODIFIERS_BASE: Abilities     = 2, 1, 0, 0, 1, 0
    ABILITIES_UPGRADED: Abilities           = 6, 0, 0, 0, 0, 0
    ABILITIES_MODIFIERS_UPGRADED: Abilities = 3, 1, 0, 0, 1, 0
    UPGRADE_PREREQUISITES: TechnologyPrerequisites = {'red':2}


class Deadnought(Ship):
    STATS_BASE: Stats      = 4, 5, 1, 1
    STATS_UPGRADED: Stats  = 4, 5, 2, 1
    STATS_MODIFIERS: Stats = 1, 1, 0, 0
    ABILITIES_BASE: Abilities               = 0, 5, 0, 0, 0, 1
    ABILITIES_UPGRADED: Abilities           = ABILITIES_BASE
    UPGRADE_PREREQUISITES: TechnologyPrerequisites = {'blue':2, 'yellow':1}


class Fighter(Ship):
    STATS_BASE: Stats      = 1, 9, 0, 0
    STATS_UPGRADED: Stats  = 1, 8, 2, 0
    STATS_MODIFIERS: Stats = 2, 1, 0, 0
    UPGRADE_PREREQUISITES: TechnologyPrerequisites = {'green':1, 'blue':1}


class Flagship(Ship):
    def __init__(self, player: Player) -> None:
        """ Retrieves the Flagship stats from the player's faction class. """
        raise NotImplementedError


class WarSun(Ship):
    STATS_UPGRADED: Stats  = 12, 3, 2, 6
    STATS_MODIFIERS: Stats = 1, 3, 0, 0
    ABILITIES_UPGRADED: Abilities           = 0, 3, 0, 0, 0, 1
    ABILITIES_MODIFIERS_UPGRADED: Abilities = 1, 3, 0, 0, 1, 0
    UPGRADE_PREREQUISITES: TechnologyPrerequisites = {'yellow':1, 'red':3}

# ---------- STRUCTURES ---------- #
class Structure(Unit):
    pass

class PDS(Structure):
    pass
    # STATS_BASE: Stats      = 0, 0, 0, 0
    # STATS_UPGRADED: Stats  = 0, 0, 0, 0
    # STATS_MODIFIERS: Stats = 1, 1, 0, 0
    # ABILITIES_BASE: Abilities               = 0, 0, 0, 0, 0, 0
    # ABILITIES_MODIFIERS_BASE: Abilities     = 1, 1, 0, 0, 1, 0
    # ABILITIES_UPGRADED: Abilities           = 0, 0, 0, 0, 0, 0
    # ABILITIES_MODIFIERS_UPGRADED: Abilities = 1, 1, 0, 0, 1, 0
    # UPGRADE_PREREQUISITES: TechnologyPrerequisites = {}

    # def __init__(self, player: Player) -> None:
    #     # unit abilities
    #     self._planetary_shield = True
    #     self._space_cannon = 6

class SpaceDock(Structure):
    STATS_BASE: Stats      = 0, 0, 0, 3
    STATS_UPGRADED: Stats  = 0, 0, 0, 3
    STATS_MODIFIERS: Stats = 1, 1, 0, 0
    ABILITIES_MODIFIERS_BASE: Abilities     = 1, 1, 0, 3, 1, 0
    ABILITIES_MODIFIERS_UPGRADED: Abilities = 1, 1, 0, 3, 1, 0
    UPGRADE_PREREQUISITES: TechnologyPrerequisites = {'yellow':2}

# ---------- GROUND FORCES ---------- #
class GroundForce(Unit):
    pass

class Infantry(GroundForce):
    STATS_BASE: Stats      = 1, 8, 0, 0
    STATS_UPGRADED: Stats  = 1, 7, 0, 0
    STATS_MODIFIERS: Stats = 2, 1, 0, 0
    UPGRADE_PREREQUISITES: TechnologyPrerequisites = {'green':2}
    ABILITY_CODE_UPGRADE = "After this unit is destroyed, roll 1 die. If the result is 6 or greater, place the unit on this card. At the start of your next turn, place each unit that is on this card on a planet you control in your home system."


if constants.POK:
    class Mech(GroundForce):
        STATS_BASE: Stats      = 2, 6, 0, 0
        STATS_UPGRADED: Stats  = STATS_BASE # just in case it's somehow upgraded
        ABILITIES_BASE: Abilities               = 0, 0, 0, 0, 0, 1
        ABILITIES_UPGRADED: Abilities           = ABILITIES_BASE
        UPGRADE_PREREQUISITES: TechnologyPrerequisites = {}

        def __init__(self, player: Player) -> None:
            """ Retrieves the Flagship stats from the player's faction class. """
            raise NotImplementedError
