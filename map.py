from system import *
from planets import *
import numpy
from using import *
from systems_and_planets import *
from typing import *

class Map():
    def __init__(self):
        # Map 
        self.map = 0
        self.tiles = 0

    def generate_map(self, map_string: str) -> None:
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

    def print_map(self, width: int, height:int):
        """
        Print out map as ascii hexagons
        width (int): number of _ characters
        height (int): how many / and \ make up the sides
        """
        # Convert adjacency map into grid based map
        # self.tiles stores tile position as its index
        # in a format related to the center of the board
        # index 0 is center, radius 0 circle
        # index 1-6 is radius 1 circle
        # index 7-18 is radius 2 circle
        # index 19-36 is radius 3 circle
        # r*6 is number of hexagons in each concentric ring
        filled = numpy.ones((9*2, 9))
        for i in range(18):
            for u in range(9):
                if i + u <= 4:
                    filled[i][u] = 0

        
        hexagon = []
        #hexagon.append('_' * width)
        for i in range(height):
            hexagon.append('/' + ' ' * (width+i*2))

        for i in range(height-1):
            hexagon.append('\\' + ' ' * (width+(height-i-1)*2))
            
        hexagon.append('\\' + '_' * width)
        hexagon_end = ['\\', '\\', '\\', '/', '/', '/']
        output = ''
        for w in range(len(filled[0])):
            if filled[0][w] and w % 2 != 0:
                output += ' ' * height + '_' * width
            else:
                output += ' ' * (height+width)
        print(output)
        for h in range(9*2):
            for line in range(height):
                output = ''
                first_fill = 1
                final_w = -1
                
                for w in range(9):
                    if filled[h][w]:
                        final_w = w
                        if (w+h) % 2 == 0:
                            # Hex Bottom
                            output += ' ' * line * first_fill + hexagon[height+line]
                            first_fill = 0
                                    
                        else:
                            # Hex Top
                            output += ' ' * (height-1-line) * first_fill + hexagon[line]
                            first_fill = 0
                        
                    else:
                        if line == 2 and final_w == -1 and filled[h+1][w]:
                            final_w = w
                            output += ' ' * height + '_' * width
                        else:
                            output += ' ' * (height+width)


                    if w == 8 and final_w != -1:
                        if (final_w+h) % 2 == 0:
                            # Hex Bottom
                            output += '/'
    
                        else:
                            # Hex Top
                            output += '\\'
                    
                        

                    
                print(output) 
            
            

    def get_map(self):
        """
        Return adjacency map, where row and column number correspond to the
        system in self.tiles
        """

        return self.map

    def get_tiles(self):
        """
        Return list of systems
        """
        return self.tiles


maps = Map()
#https://keeganw.github.io/ti4
##map_input = input("Enter map string: ")
##maps.generate_map(map_input)
##print(maps.get_map())
##print(maps.get_tiles())
maps.print_map(8, 3)
def hexagon_sizes():
    for u in range(1, 10):
        for i in range(1, 20):
            ratio = (u*2*2)/(i+u*2)
            if ratio == 0.8:
                print(i,u)
                print(ratio)
                maps.print_map(i, u)

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
