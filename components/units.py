class Unit:
    def __init__(self):
        self.cost = 0
        self.combat = 0
        self.combat_multiplier = 1
        self.move = 0
        self.capacity = 0
        self.type = ""
        self.carrying = []

class Ship(Unit):
    pass

class Deadnought(Ship):
    pass

class WarSun(Ship):
    pass

class Flagship(Ship):
    pass

class Fighter(Ship):
    pass

class Destroyer(Ship):
    pass

class Carrier(Ship):
    pass

class Cruiser(Ship):
    pass

class Structure(Unit):
    def hello(self):
        pass

class Ground_Force(Unit):
    pass
