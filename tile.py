from typing import *
from planet import *

class Tile():
    def __init__(self, id: int, name: str, anomalies: List[str], planets: List[Planet], wormholes: List[str], token: bool) -> None:
        self.id = id
        self.name = name
        self.anomalies = anomalies
        self.planets = planets
        self.wormholes = wormholes
        self.has_frontier_token = token

    def become_nova(self) -> None:
        '''Turn tile into Muaat Supernova'''
        self.name = 'Muaat Supernova'
        self.anomalies = 'supernova'
        oldplanets = self.planets
        oldwormholes = self.wormholes
        self.planets = None
        self.wormholes = None
        return ((oldplanets,oldwormholes))

    def add_wormhole(self, type: str) -> None:
        self.wormholes.append(type)

    def add_planet(self, planet: Planet) -> None:
        self.planets.append(planet)

    def remove_planet(self, planet_name: str) -> None:
        self.planets.remove(self.planets.get_name())

    def explore(self):
        '''Removes frontier token'''
        self.has_frontier_token = False

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

    #__repr__ and __str__ can come later.