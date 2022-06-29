import sys
sys.path.append('components/')

# is someone changing these imports? Please tell me -Darcy
from components.system import *
from components.planets import *
import numpy as np
from constants import *
from components.systems_and_planets import *
from typing import *
np.set_printoptions(threshold=np.inf)
# 0 represents there being no tile
DEFAULT_MAP = "41 71 62 67 75 38 47 40 37 25 27 50 72 66 78 68 74 39 60 32 0 44 23 30 0 59 61 0 26 79 0 21 63 73 0 20"

class Map():
    def __init__(self):
        # Map 
        # self.map and self.adjacencies are two different stores for which tile is adjacent to which
        # self.map stores each tile's relation to every other tile
        # self.adjacencies is a dictionary of sets which stores the tile id for every tile a tile is adjacent to
        # self.adjacencies is Riley's prefered type for creating the distance algorithm

        self.map = []
        self.adjacencies = ADJACENCIES_TEMPLATE
        self.tiles = []


    def generate_map(self, map_string=DEFAULT_MAP) -> None:
        """
        Generate list of tiles and an adjacency matrix from map string
        """
        # Mecatol Rex always at center of board
        # and not included in map string

        # Map string: index is tile position, value is tile type 
        map_string = "18 " + map_string
        map_string = map_string.split(' ')

        size = len(map_string)

        # index of wormholes in self.tiles
        alpha_wormhole_pos = []
        beta_wormhole_pos =[]


        self.map = np.zeros((size, size))
        # index represents position in a spiral outwards from map center
        # see print_map for more details
        self.tiles = []
        # index represent position on board
        # number at index represent TI tile id

        # For every number in map_string turn it into a tile and
        # add it to self.tiles
        # also add which tiles it is adjacent too into self.map and self.adjacencies
        for position in range(size):
            # id is tile type
            id = map_string[position]
            if id != "0":
                system = System(id, position)
                # for testing purposes
                system.add_unit(Carrier(0))

                self.tiles.append(system)

                # if tile is a wormhole store it for later
                if id in ALPHA:
                    alpha_wormhole_pos.append(position)

                elif id in BETA:
                    beta_wormhole_pos.append(position)

            else:
                # if tile is empty
                self.tiles.append(0)

            # Alter adjacency map
            if id != "0":
                if id not in HYPERLANES:
                    # For each adjacent tile
                    for adj_position in ADJACENCY_DATA[str(position)]:
                        if adj_position < size and map_string[adj_position] not in HYPERLANES and map_string[adj_position] != "0":
                            self.map[position][adj_position] = 1
                            self.map[adj_position][position] = 1

                            adj_id = map_string[adj_position]
                            self.adjacencies[str(position)].add(adj_position)
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
                        
                        self.adjacencies[str(start_id)].add(end_id)
                        self.adjacencies[str(end_id)].add(start_id)
        print(self.adjacencies)



        # index is what index the wormholes are at in self.tiles
        # for each wormhole set it to be adjacent to the others
        for index in alpha_wormhole_pos:
            for adj_index in alpha_wormhole_pos:
                if index != adj_index:
                    self.map[index][adj_index] = 2
                    self.map[adj_index][index] = 2

                    id = map_string[index]
                    adj_id = map_string[adj_index]
                    self.adjacencies[id].add(adj_id)
                    self.adjacencies[adj_id].add(id)


    def print_map(self, width: int, height:int):
        """
        Print out map as ascii hexagons
        width (int): length of top and bottom face in _ characters
        height (int): how many lines make up 1 of the side faces
        """
        # Convert adjacency map into grid based map
        # self.tiles stores tile position as its index
        # in a format related to the center of the board
        # index 0 is center, radius 0 circle
        # index 1-6 is radius 1 circle
        # index 7-18 is radius 2 circle
        # index 19-36 is radius 3 circle
        # r*6 is number of hexagons in each concentric ring
        filled = np.zeros((9*2, 9))
        # Center of map always has tile
        filled[8][4] = 1
        filled[9][4] = 1

        # Represent moving in a hexagonal circle on our grid
        DIRECTIONS = [(1, 1), (2, 0), (1, -1), (-1, -1), (-2, 0), (-1, 1)]

        # start from index 1 tile above center at top hexagon
        y = 6
        x = 4

        # stay and offset control where the hexagonal spiral is
        stay = 1
        offset = 0
        for i in range(len(self.tiles)-1):
            # when reach the end of the spiral jump to the next
            if i == offset + 6*stay:
                offset = i
                stay += 1
                y += -2

            if self.tiles[min(i+1, len(self.tiles)-1)] != 0:
                filled[y][x] = i+1
                filled[y+1][x] = i+1
            # move in a hexagonal spiral
            # as stay increases stay in a single direction for longer
            x += DIRECTIONS[((i-offset) // stay) % 6][1]
            y += DIRECTIONS[((i-offset) // stay) % 6][0]

        # Create list containing base hexagon shape
        # each line corresponds to part of the shape
        # This part of the code is where information about each tile could be added
        hexagon = []
        for i in range(height):
            hexagon.append('/' + ' ' * (width+i*2))

        for i in range(height-1):
            hexagon.append('\\' + ' ' * (width+(height-i-1)*2))

        hexagon.append('\\' + '_' * width)
        hexagon_end = ['\\', '\\', '\\', '/', '/', '/']
        map_list = []
        # Print the top of the first line of hexagons
        output = ''
        for w in range(len(filled[0])):
            if filled[0][w] and w % 2 == 0:
                output += ' ' * height + '_' * width
            else:
                output += ' ' * (height+width)
        map_list.append(output)

        # Imagining the hexagonal grid as instead a grid of half hexagons
        # that alternate up and down along x and y axis
        # max board size is 9x9 hexagons, so grid is 18x9 since we split hexagons
        # horizontally

        # Grid is 0,0 at top left corner and max, max at bottom right
        for h in range(9*2):
            # The lines making up half a hexagon = height
            for line in range(height):
                output = ''
                # Hexagon segmenets do not have padding spaces
                # so each line the first time we print a segement
                # we need to add spaces, how many depends on current hexagon
                # orientation
                first_fill = 1

                # Segements assume the right most piece will be filled by another
                # segement. Since final segement will not have another piece to
                # the right we need to add it later. Orientation of piece will
                # depend on current hexagon orientation
                final_w = -1

                for w in range(9):
                    if filled[h][w]:
                        final_w = w
                        if (w+h) % 2 != 0:
                            # Hex Bottom
                            output += ' ' * line * first_fill + hexagon[height+line]
                            first_fill = 0

                        else:
                            # Hex Top
                            output += ' ' * (height-1-line) * first_fill + hexagon[line]
                            first_fill = 0

                    else:
                        # if on a non-filled tile and last tile was filled complete the last tile
                        # add a top to a hexagon if below current position is filled
                        if final_w == -1:
                            if line == height-1 and filled[min(h+1, 17)][w]:
                                output += ' ' * height + '_' * width
                            else:
                                output += ' ' * (height+width)

                        elif final_w + 1 == w:
                            if (w+h) % 2 != 0:
                                # Hex Bottom
                                if filled[min(h+1, 17)][w] or line < height-1:
                                    output += hexagon[height+line]
                                else:
                                    output += '\\' + ' '*width
                            else:
                                # Hex Top
                                output += ' ' * (height-1-line) * first_fill + hexagon[line]

                        elif line == height-1 and filled[min(h+1,17)][w]:
                            output += ' ' + '_'*width
                            final_w = -2

                    # since tiles are completed by the subsequent tile
                    # in the final column the right of the hexagons will be unfilled
                    # so we fill them
                    if w == 8 and final_w == 8:
                        if final_w == -2:
                            continue
                        if (final_w+h) % 2 != 0:
                            # Hex Bottom
                            output += '/'

                        else:
                            # Hex Top
                            output += '\\'
                map_list.append(output)
        print(filled)
        completed_tiles = []

        # Go through the hex grid and add information about each tile
        # Probably really inefficient
        for i in range(len(map_list)):
            #For every hexagon find text need
            if i % (height) == 1:
                row = (i-1) // height
                for u in range(len(filled[row])):
                    if filled[row][u] and filled[row][u] not in completed_tiles:
                        textagon = []
                        
                        system = self.tiles[int(filled[row][u])]
                        units = system.get_units()
                        # Put the unit type and number into the system
                        for unit in units:
                            textagon.append(unit.char() + str(units[unit]))



                        textagon.append(str(filled[row][u]))
                        
                        # add wormhole support
                        # add planetsupport
                        activated = system.activated_by()
                        for p in activated:
                            textagon.append(str(p))

                        # Loops through each line of that makes up the hexagon and prints centered text so that it fits within the hexagon
                        for line in range(height*2):
                            if len(textagon) == 0:
                                break
                            # alter is original line
                            alter = map_list[i+line]
                            # alter1 is everything to the left of the hexagon
                            # alter 2 is everything to the right of the hexagon
                            # this results in alter1+alter2 being everything in alter except for the spaces inside the hexagon
                            alter1 = alter[:(height+u*(height+width))]
                            alter2 = alter[((u+1)*(width+height)):]

                            #
                            middle = ''
                            pop_num = 0
                            for text in textagon:
                                if len(middle+text)+1 < width:
                                    middle += text + ' '
                                    pop_num += 1

                            for k in range(pop_num):
                                textagon.pop(0)


                            # Adds centered text to the hexagon
                            offset = width-len(middle)
                            for t in range(offset):
                                if t < (offset/2):
                                    middle = ' ' + middle
                                else:
                                    middle += ' '
                            map_list[i+line] = alter1 + middle + alter2
                        completed_tiles.append(filled[row][u])


            print(i, map_list[i])

    def get_map(self):
        """
        Return adjacency map, where row and column number correspond to the
        system in self.tiles
        """

        return self.map

    def get_systems(self):
        """
        Return list of systems
        """
        return self.tiles

    def get_distance(self, origin: int, destination: int):
        # Takes the ids of the origin and destination tiles and returns the shortest distance

        # Currently does not account for:
        # gravity rifts
        # other anomolies which inhibit movement
        # other players' ships which inhibit movement
        # the argent flight's tech which inhibits movement
        visited = VISITED_TEMPLATE
        queue = [(str(origin), 0)]

        while True:
            tile = queue[0][0]
            distance = queue[0][1]
            queue.pop(0)

            if tile == str(destination):
                return distance

            if not visited[tile]:
                visited[tile] = True
                for adjacent_tile in self.adjacencies[tile]:
                    queue.append((adjacent_tile, distance+1))

    def is_adjacent(self, system1_id: int, system2_id: int) -> bool:
        """
        Returns whether system1 is adjacent to system 2
        """
        if system2_id in self.adjacencies[str(system1_id)]:
            return True

        return False
        





#Testing
maps = Map()
#https://keeganw.github.io/ti4
map_input = input("Enter map string: ")
if map_input != '':
    maps.generate_map(map_input)
else:
    maps.generate_map()

maps.print_map(14, 5)

