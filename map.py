from system import *
from planets import *
import numpy
from using import *


class Map():
    def __init__(self):
        # Map 
        self.map = 0
        self.tiles = 0

    def generate_map(self, map_string):
        # Mecatol Rex always at center of board
        # and not included in map string
        map_string = "18 " + map_string
        map_string = map_string.split(' ')
        print(map_string)
        size = len(map_string)

        self.map = numpy.zeros((size, size))
        self.tiles = []
        # index represent position on board
        # number at index represent TI tile id
        
        for position in range(len(map_string)):
            if map_string[position] != "0":
                self.tiles.append(System(map_string[position], position))
            else:
                self.tiles.append(0)
                
            for adj_position in ADJACENCY_DATA[str(position)]:
                if adj_position < size:
                    self.map[position][adj_position] = 1
                    self.map[adj_position][position] = 1

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
