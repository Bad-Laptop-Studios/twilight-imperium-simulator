import using

class Faction():
    def __init__(self):
        self._name = None
        self._abilities = None
        self._promissory_note = None
        self._faction_technologies = None
        self._faction_units = None
        self._flagship = None
        if using.POK:
            self.mech = None
            self.learders = None

        self._commodities = None
        self._starting_units = None
        self.starting_technologies = None
        self.starting_planets = None


        self.quote = None
        self.lore = None

        pass

    def get_commodities(self) -> int:
        """ Returns the faction's default commodity value. """
        return self.commodities

class TitansOfUl(Faction):
    def __init__(self):
        pass