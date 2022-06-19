from typing import *
from planets import *
from systems_and_planets import *
from units import *
class System():
    def __init__(self, TI_id: str, id: int) -> None:
        """
        self, id: int, name: str, anomalies: List[str], planets: List[Planet], wormholes: List[str], token: bool)

        Creates a system using its TI_id using data found in systems_and_planets.py
        """
        system_data = SYSTEMS[TI_id]
        self.TI_id = TI_id
        self.id = id
        self.activated = []
        self.wormholes = system_data["wormhole"]
        self.anomalies = self._determine_anomalies(TI_id)

        self.planets = []
        for i in range(len(system_data["planets"])):
            self.add_planet(Planet(TI_id, i))

        self.name = TI_id
        self.has_frontier_token = False

        self.ships = []
        
    def _determine_anomalies(self, TI_id: int) -> List[str]:
        anomalies = []
        if TI_id in ["44", "45", "79"]:
            anomalies.append("asteriodFields")
        elif TI_id in ["41", "67"]:
            anomalies.append("gravityRifts")
        elif TI_id in ["42", "68"]:
            anomalies.append("nebulae")
        elif TI_id in ["43", "80"]:
            anomalies.append("supernova")
        return anomalies

    def become_nova(self) -> Tuple[List[Planet], List[str]]:
        """ Turn system into Muaat Supernova. """
        self.name = 'Muaat Supernova'
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

    def add_ships(self, ships: List[Unit]):
        for unit in ships:
            self.ships.append(unit)


    #Return Functions
    def get_id(self) -> int:
        return self.id
    def get_TI_id(self) -> str:
        return self.TI_id
    def get_name(self) -> str:
        return self.name
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
