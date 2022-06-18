class Tile():
    def __init__(self):
        self.asteroid_field = None
        self.nebula = None
        #etc

class Planet():
    def __init__(self):

        self.name = None
        self.resource = None
        self.influence = None
        self.flavour_text = None

        # planet types - a planet can be all three at once
        self.cultural = False
        self.hazardous = False
        self.industrial = False

        # planet technologies - a planet can be all four at once
        self.blue = False
        self.green = False
        self.red = False
        self.yellow = False

        self.exhausted = False
