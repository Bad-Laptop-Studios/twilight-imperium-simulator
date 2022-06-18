from typing import List
from factions import *

class Planet():
    def __init__(self, name):
        self._name = name
        self._resource = None
        self._influence = None
        self._flavour_text = None
        self._faction = None
        self._type = []
        self._technology_specialty = []
        self._attachement = None
        self._is_exhausted = False

        # planet types - a planet can be all three at once
        # self._cultural = False
        # self._hazardous = False
        # self._industrial = False

        # planet technologies - a planet can be all four at once
        # self._blue = False
        # self._green = False
        # self._red = False
        # self._yellow = False

    def _fill_planet_details(self):
        """ Given the planet name, fills out the planet details. Uses planets.json. """
        raise NotImplementedError # planets.json does not exist yet

    def get_name(self) -> int:
        """ Returns the name of the planet. """
        return self._name

    def get_resource(self) -> int:
        """ Returns the default resource value of the planet. """
        return self._resource

    def get_influence(self) -> int:
        """ Returns the default influence value of the planet. """
        return self._influence

    def get_type(self) -> List[str]:
        """ Returns the planet types of the planet. """
        # """ Returns the list of planet types for the planet. """
        return self._type

    def get_technology_specialty(self) -> List[str]:
        """ Returns the technology specialty of the planet. """
        # """ Returns the list of technology specialty for the planet. """
        return self._technology_specialty

    def get_is_exhausted(self) -> bool:
        """ Returns whether the planet is exhausted or not. """
        return self._is_exhausted

    def set_is_exhausted(self, exhaustion: bool) -> None:
        """ Sets the exhaustion of the planet. """
        self._is_exhausted = exhaustion