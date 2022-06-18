class Unit:
    def __init__(self):
        self.cost = 0
        self.combat = 0
        self.combat_multiplier = 1
        self.move = 0
        self.capacity = 0
        self.type = ""
        self.carrying = []

class Structure(Unit):
    def hello(self):
        pass

class Ground_Force(Unit):
    pass
