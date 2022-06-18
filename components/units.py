import using

class Unit:
    def __init__(self):
        # unit stats
        self._cost, self._combat, self._move, self._capacity = 0, 0, 0, 0
        self._cost_units = 1
        self._combat_burst = 1

        # unit abilities
        self._bombardment, self._bombardment_multiplier                   = 0, 1
        self._production, self._production_bonus                          = 0, 0
        self._space_cannon, self._space_cannon_multiplier                 = 0, 1
        self._anti_fighter_barrage, self._anti_fighter_barrage_multiplier = 0, 1
        self._can_sustain = False
        self._planetary_shield = False

        # unit status
        self._is_sustained = False
        self._player = None

        self._type = ""
        self._carrying = []

    def has_sustained(self) -> bool:
        """ Returns whether or not the unit has sustained damage. """
        return self._is_sustained


# ---------- SHIPS ---------- #
class Ship(Unit):
    pass

class Deadnought(Ship):
    def __init__(self) -> None:
        # unit stats
        self._cost, self._combat, self._move, self._capacity = 4, 5, 1, 1

        # unit abilities
        self._can_sustain = True
        self._bombardment = 5

class WarSun(Ship):
    pass

class Flagship(Ship):
    pass

class Fighter(Ship):
    def __init__(self) -> None:
        # unit stats
        self._cost, self._combat, self._move, self._capacity = 1, 9, 0, 0

class Destroyer(Ship):
    def __init__(self) -> None:
        # unit stats
        self._cost, self._combat, self._move, self._capacity = 1, 9, 2, 0

        # unit abilities
        self._anti_fighter_barrage, self._anti_fighter_barrage_multiplier = 9, 2

class Carrier(Ship):
    def __init__(self) -> None:
        # unit stats
        self._cost, self._combat, self._move, self._capacity = 3, 9, 1, 4

class Cruiser(Ship):
    def __init__(self) -> None:
        # unit stats
        self._cost, self._combat, self._move, self._capacity = 2, 7, 2, 0

# ---------- STRUCTURES ---------- #
class Structure(Unit):
    pass

class PDS(Structure):
    def __init__(self) -> None:
        # unit abilities
        self._planetary_shield = True
        self._space_cannon = 6

class SpaceDock(Structure):
    def __init__(self) -> None:
        # unit abilities
        self._production_bonus = 2

# ---------- GROUND FORCES ---------- #
class GroundForce(Unit):
    pass

class Infantry(GroundForce):
    def __init__(self) -> None:
        # unit stats
        self._cost, self._combat, self._move, self._capacity = 1, 8, 0, 0
        self._cost_units = 2

if using.POK:
    class Mech(GroundForce):
        """ CLASS IS INCOMPLETE - ALL MECHS ARE DIFFERENT"""
        def __init__(self) -> None:
            # unit stats
            self._cost, self._combat, self._move, self._capacity = 2, 6, 0, 0

            # unit abilities
            self._can_sustain = True

