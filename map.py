from system import *
from planets import *
import numpy
from using import *
from systems_and_planets import *

class Map():
    def __init__(self):
        # Map 
        self.map = 0
        self.tiles = 0

    def generate_map(self, map_string):
        """
        Generate list of tiles and adjacency matrix from map string
        """
        # Mecatol Rex always at center of board
        # and not included in map string
        map_string = "18 " + map_string
        map_string = map_string.split(' ')
        print(map_string)
        size = len(map_string)

        # index of wormholes in self.tiles
        alpha_wormhole_pos = []
        beta_wormhole_pos =[]
        
        
        self.map = numpy.zeros((size, size))
        self.tiles = []
        # index represent position on board
        # number at index represent TI tile id
        
        for position in range(len(map_string)):
            id = map_string[position]
            if id != "0":
                self.tiles.append(System(id, position))

                if id in ALPHA:
                    alpha_wormhole_pos.append(position)
                
                elif id in BETA:
                    beta_wormhole_pos.append(position)
                    
            else:
                self.tiles.append(0)

            # Alter adjacency map
            if id not in HYPERLANES:
                for adj_position in ADJACENCY_DATA[str(position)]:
                    if adj_position < size:
                        self.map[position][adj_position] = 1
                        self.map[adj_position][position] = 1
            else:
                hyperlanes = SYSTEMS[id]["hyperlanes"]
                # A Hyperlane consists of two variables representing which faces
                # are connected
                # Finds systems that connected to the hyperlane and makes them
                # adjacent
                for hyperlane in hyperlanes:
                    start = ADJACENCY_DATA[str(position)][hyperlane[0]]
                    end = ADJACENCY_DATA[str(position)][hyperlane[1]]
                    self.map[start][end] = 1
                    self.map[end][start] = 1
                    
        for index in alpha_wormhole_pos:
            for adj_index in alpha_wormhole_pos:
                if index != adj_index:
                     self.map[index][adj_index] = 2
                     self.map[adj_index][index] = 2
                     
        for index in beta_wormhole_pos:
            for adj_index in beta_wormhole_pos:
                if index != adj_index:
                     self.map[index][adj_index] = 2
                     self.map[adj_index][index] = 2

    def print_map(self):
        print("map")

    def get_map(self):
        return self.map

    def get_tiles(self):
        return self.tiles


maps = Map()
#https://keeganw.github.io/ti4
map_input = input("Enter map string: ")
maps.generate_map(map_input)
print(maps.get_map())
print(maps.get_tiles())
"""    __
    __/ff\__             
 __/  \__/  \
/  \__/  \__/             
  _____      _____
 /ddddd\    /     d\
/ddddddd\  /       d\
\ddddddd/  \dddddddd/
 \_____/    \______/

   ________
  /        \
 /          \
/            \
\            /
 \          /
  \________/
"""
