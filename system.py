from typing import *
from planets import *

class system():
    def __init__(self, id: int, name: str, anomalies: List[str], planets: List[Planet], wormholes: List[str], token: bool) -> None:
        self.id = id
        self.name = name
        self.anomalies = anomalies
        self.planets = planets
        self.wormholes = wormholes
        self.has_frontier_token = token
        self.activated = []

    def become_nova(self) -> Tuple[List[Planet], List[str]]:
        """Turn system into Muaat Supernova."""
        self.name = 'Muaat Supernova'
        self.anomalies = 'supernova'
        oldplanets = self.planets
        oldwormholes = self.wormholes
        self.planets = None
        self.wormholes = None
        return ((oldplanets,oldwormholes))

    def add_wormhole(self, type: str) -> None:
        """Adds a wormhole of the given type to a system."""
        self.wormholes.append(type)

    def add_planet(self, planet: Planet) -> None:
        """Adds the given planet object to the system."""
        self.planets.append(planet)

    def remove_planet(self, planet_name: str) -> None:
        """Removes a planet with the given name from the system."""
        for p in self.planets:
            if p.get_name() == planet_name:
                self.planets.remove(p)

    def explore(self) -> None:
        """Removes the frontier token from the system."""
        self.has_frontier_token = False
    
    def activate(self, player_id: int) -> None:
        """Adds a player to the current activated list."""
        self.activated.append(player_id)
    
    def deactivate_all(self) -> None:
        """Removes all players from the activated list."""
        self.activated = []


    #Return Functions
    def get_id(self) -> int:
        return self.id
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