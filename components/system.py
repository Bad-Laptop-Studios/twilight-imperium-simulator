import sys
sys.path.insert(0, 'D:/Documents/GitHub/twilight-imperium-simulator')

from typing import *
from planets import *
from systems_and_planets import *
from units import *
class System():
    def __init__(self, system_id: str, id: int) -> None:
        """
        self, id: int, name: str, anomalies: List[str], planets: List[Planet], wormholes: List[str], token: bool)

        Creates a system using its system_id using data found in systems_and_planets.py
        """
        system_data = SYSTEMS[system_id]
        self.system_id = system_id
        self.id = id
        self.activated = []
        self.wormholes = system_data["wormhole"]
        self.anomalies = self._determine_anomalies(system_id)

        self.planets = []
        for i in range(len(system_data["planets"])):
            self.add_planet(Planet(system_id, i))
        self.has_frontier_token = False


        # Store units in system as a dictionary
        self.units = {}
        
    def _determine_anomalies(self, system_id: int) -> List[str]:
        anomalies = []
        if system_id in ["44", "45", "79"]:
            anomalies.append("asteriodFields")
        elif system_id in ["41", "67"]:
            anomalies.append("gravityRifts")
        elif system_id in ["42", "68"]:
            anomalies.append("nebulae")
        elif system_id in ["43", "80"]:
            anomalies.append("supernova")
        return anomalies

    def become_nova(self) -> Tuple[List[Planet], List[str]]:
        """ Turn system into Muaat Supernova. """
        self.anomalies = 'supernova'
        oldplanets = self.planets
        oldwormholes = self.wormholes
        self.planets = None
        self.wormholes = None
        return ((oldplanets,oldwormholes))

    def add_wormhole(self, type: str) -> None:
        """ Adds a wormhole of the given type to a system. """
        self.wormholes.append(type)

    def add_planet(self, planet: Planet) -> None:
        """Adds the given planet object to the system."""
        self.planets.append(planet)

    def remove_planet(self, planet_name: str) -> None:
        """ Removes a planet with the given name from the system. """
        for p in self.planets:
            if p.get_name() == planet_name:
                self.planets.remove(p)

    def explore(self) -> None:
        """ Removes the frontier token from the system. """
        self.has_frontier_token = False
    
    def activate(self, player_id: int) -> None:
        """ Adds a player to the current activated list. """
        self.activated.append(player_id)
    
    def deactivate_all(self) -> None:
        """ Removes all players from the activated list. """
        self.activated = []

    def add_unit(self, unit_type: Unit, number: int = 1):
        """
        Add a unit to the units dictionary
        """
        if unit_type in self.units:
            self.units[unit] += number

        else:
            self.units[unit_type] = 1

    def remove_unit(self, unit_type: Unit, number: int) -> None:
        """
        Remove a number of units from the system
        """
        self.units[unit_type] -= number
        if self.units[unit_type] <= 0:
            del self.units[unit_type]


    #Return Functions
    def get_id(self) -> int:
        return self.id
    def get_system_id(self) -> str:
        return self.system_id
    def get_units(self) -> Dict:
        return self.units.copy()
    def get_anomalies(self) -> List[str]:
        return self.anomalies
    def get_planets(self) -> List[Planet]:
        return self.planets
    def get_wormholes(self) -> List[str]:
        return self.wormholes
    def has_token(self) -> bool:
        return self.has_frontier_token
    def activated_by(self) -> List[int]:
        """Returns the numeric representation of the players that have activated this system"""
        return self.activated

    #__repr__ and __str__ can come later.
