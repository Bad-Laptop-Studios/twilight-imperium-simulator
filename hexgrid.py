""" Module for map support. Manages hexagon and grid representations of the map. """


from functools import cache
from typing import Literal
import numpy as np
from math import ceil, sqrt
from components.systems_and_planets import SYSTEMS
from constants_ascii import *
import textwrap

TileID = str

MAP_STRING = "1"
MAP_STRING = "1 2 3 4 5 6 7"
MAP_STRING = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19"
MAP_STRING = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37"
MAP_STRING = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61"
# or you can use https://keeganw.github.io/ti4
MAP_STRING = "18 30 26 40 79 38 71 68 48 76 80 69 47 62 25 34 43 37 28 0 61 73 0 50 21 0 45 77 0 29 42 0 23 49 0 20 60"
MAP_STRING = "18 24 50 19 21 66 23 49 63 65 22 77 20 78 46 19 59 50 62"
MAP_STRING = "18 28 77 36 63 30 66 35 23 27 32 31 20 37 29 34 50 38 49 0 19 48 0 69 21 0 75 46 0 65 47 0 33 22 0 76 78"
MAP_LIST = MAP_STRING.split()

def spiral_length_to_rings(spiral_length: int) -> int:
    """ Return minimum rings for map.
    For spiral_length <1, rings is minimal, but map printout won't be.

    Parameters:
        spiral_length: length of TTS string"""
    if spiral_length <= 0: return 0
    return ceil((sqrt(12 * spiral_length - 3) - 3) / 6)       # rearranged formula from https://oeis.org/A003215 (scroll down for visual)

def ring_to_circumference(ring: int) -> int:
    """ Return circumference for ring number. 
    Assumes ring is non-negative. """
    if not ring:
        return 1
    else:
        return 6 * ring         # of note: https://oeis.org/A008458 (scroll down for visual)

def add(v1: tuple[int, ...], v2: tuple[int, ...]) -> tuple[int, ...]:
    """ Add tuples elementwise. """
    return map(sum, zip(v1, v2))

def spiral_to_tile_grid(map_spiral) -> np.ndarray:
    """ Convert TTS string (tiles in a clockwise hexagonal spiral) to a grid for printing. """
    RING_MAX = spiral_length_to_rings(len(map_spiral))
    array_size = 2 * RING_MAX + 1
    tile_grid = np.full((array_size, array_size), "-1", dtype=object)

    centre = array_size // 2
    origin = centre, centre
    x, y = origin               # x is vertical, y is horizontal
    ring = 0                    # also how many tiles per side
    side = 0
    arc = 0                     # number of tiles around the circumference
    side_arc = 0                # number of tiles along the side
    vector = None               # the vector by which x and y move on the grid to account for this being a hexagonal map
    for tile_id in map_spiral:
        """ Put tile_id in grid. Then calculate values for next tile. """
        # print(f"ring:{ring}, arc:{arc}, side:{side}, pos:{x,y}, vector:{vector}, tile_id:{tile_id}, side_arc:{side_arc}")
        # print(tile_grid)
        tile_grid[x, y] = tile_id

        circumference = ring_to_circumference(ring)
        if arc >= circumference - 1 or ring == 0:       # -1 due to index from 0
            """ Ring is full, reset and go to next ring. """
            arc = side = -1
            # vector = None                                   # for debugging
            ring += 1
            x,y = add(origin, (-ring,0))                    # go to top of next ring
        else:
            """ Stay on this ring. """
            side_arc = arc % ring
            side += not side_arc                            # next side if current tile is a corner

            # optimised version: only calculate what we need
            # incorrect now. Update to match unoptimised version
            # j = (side % 3 + 1) % 2 - 2 * (2 <= side <= 3)
            # i = ((ring * (side % 3 == 2) + side_arc) % 2) ** abs(j) - 1 * (side >= 3) - (side == 4)
            # vector = (i, j)

            # unoptimised version: better demonstrates how vector is calculated.
            # see link for how coordinates system works - every 2nd column of hexagons is shifted up half a hexagon to make a grid: https://codegolf.stackexchange.com/questions/70166/draw-and-label-an-ascii-hexagonal-grid
            vector_table = [((RING_MAX + side_arc) % 2, 1), (1, 0), ((RING_MAX + ring + side_arc) % 2, -1), ((RING_MAX + side_arc) % 2 - 1, -1), (-1, 0), ((RING_MAX + ring + side_arc) % 2 - 1, 1)]
            vector = vector_table[side]
            x,y = add((x,y), vector)                        # go to next tile position

        arc += 1
    # print(tile_grid)
    return tile_grid

def tile_grid_to_map_grid(tile_grid: np.ndarray) -> np.ndarray:
    """"""
    shape = rows, cols = tile_grid.shape
    # map_grid = np.full(*shape, "", dtype=object)      Python 3.11
    map_grid = np.full((rows, cols), {}, dtype=object)

    # for position, tile_id in np.ndenumerate(tile_grid):       Python 3.11
    #     map_grid[*position] = SYSTEMS[tile_id]
    for (row_index, col_index), tile_id in np.ndenumerate(tile_grid):
        map_grid[row_index, col_index] = {"id": tile_id} | SYSTEMS[tile_id]
    
    return map_grid
    


def map_grid_to_ascii(map_grid) -> str:
    """
                                       ,-- base(0,0)
                                       v
                 corner(0,0,0) -->  .-----.  <-- corner(0,0,1)
              diagonal(0,0,0) -->  /       \  <-- diagonal(0,0,1)
                                  {   0,0   }-----.  <-- corner(0,1,1)
                                   \       /       \  <-- diagonal(0,1,1) - all diagonals on the same edge have the same position
                                    }-----{   0,1   }  <-- corner(1,2,0)
                                   /       \       /
                                  {   1,0   }-----'
                                   \       /   ^-- base(1,1)
                                    '-----' 

    TODO:
        Change inside() argument order to row_index, col_index, line_index
        (Maybe) Rename corner_index and diagonal_index to corner_parity and diagonal_parity
    """

    # ---------- components ---------- #
    def bases(row_index, line_index):
        """"""
        def corner(row_index, col_index, corner_index) -> str:
            """ Return corner of hexagon in ASCII.
            
            Parameters:
                row_index: row_index for hexagon below corner
                col_index: col_index for hexagon below corner
                corner_index: 0 for left, 1 for right
            """
            # get neighbour positions, rotating initially upwards from (row_index, col_index)
            neighbours = ((row_index, col_index),
                          (row_index - 1, col_index),
                          (row_index - (not col_index % 2), col_index + 2 * corner_index - 1))
            
            # determine whether neighbours are present (and where)
            count = share_count(neighbours)
            is_below = share_count((neighbours[0],))
            is_above = share_count((neighbours[1],))

            # return characters
            if not count:
                return ' '
            elif count == 1 and (is_below ^ is_above):
                return '.' if is_below else '\''
            else:
                return '{' if corner_index else '}'

        def base(row_index, col_index) -> str:
            """ Return base of hexagon in ASCII.

            Parameters:
                row_index: row_index for hexagon below the base
                col_index: col_index for hexagon
            """
            # get neighbour positions, starting with (row_index, col_index)
            neighbours = ((row_index, col_index),
                          (row_index - 1, col_index))

            # determine whether neighbours are present
            count = share_count(neighbours)

            # return characters
            if not count:
                return X_SCALE * ' '
            return X_SCALE * '—'  # em-dash


        # parity describes whether the first column started with a hexagon base (0) or inside (1)
        parity = bool(line_index)

        # Demonstration for algorithm below. Here, X_SCALE = 3, Y_SCALE = 2
        # 0 parity: ascii_line = "  ."              + cols // 2 * "———{       }" + "———."
        # 1 parity: ascii_line = "{"   + "       }" + cols // 2 * "———{       }"

        ascii_line = buffer(line_index) + corner(row_index, -parity, parity)
        # add a hexagon inside that advances by one column to align with the hexagon bases
        if parity:
            ascii_line += inside(row_index, 0, Y_SCALE) + corner(row_index, 1, 0)
        # add aligned columns in groups of two
        for col_index in range(parity, cols - 1, 2):
            ascii_line += base(row_index, col_index) + corner(row_index, col_index, 1) + inside(row_index - 1 + parity, col_index + 1, Y_SCALE) + corner(row_index, col_index + 2, 0)
        # add a hexagon base that advances by one column to align with the hexagon insides
        if not parity:
            ascii_line += base(row_index, cols - 1) + corner(row_index, cols - 1, 1)
        ascii_line += '\n'
            
        return ascii_line


    def insides(row_index, line_index):
        """"""
        def diagonal(row_index: int, col_index: int, diagonal_index: Literal[0, 1]) -> str:
            """ Return diagonal of hexagon in ASCII.
            
            Parameters:
                row_index: row_index for hexagon below diagonal
                col_index: col_index for hexagon below diagonal
                diagonal_index: 0 for left (/), 1 for right (\)
            """
            # get neighbour positions, clockwise from (row_index, col_index)
            neighbours = ((row_index, col_index),
                          (row_index - (not col_index % 2), col_index + 2 * diagonal_index - 1))
                        # (row_index [- 1], col_index +/- 1)

            # determine whether neighbours are present
            count = share_count(neighbours)

            # return characters
            if not count:
                return ' '
            return '\\' if diagonal_index else '/'


        # line_index parity describes whether the first column started with a hexagon top (0) or bottom (1) half
        parity = line_index >= Y_SCALE
        # lines_to_top/bottom_base describe the first column
        lines_to_top_base = line_index - parity * Y_SCALE
        lines_to_bottom_base = line_index + (not parity) * Y_SCALE

        # Demonstration for algorithm below. Here, X_SCALE = 3, Y_SCALE = 2
        # 0 parity: ascii_line = " /"            + cols // 2 * "     \     /" + "     \"
        # 1 parity: ascii_line = " \" + "     /" + cols // 2 * "     \     /"

        ascii_line = buffer(line_index) + diagonal(row_index, -parity, parity)
        # add a lower hexagon half that advances by one column to align with the upper hexagon halves
        if parity:
            ascii_line += inside(row_index, 0, line_index) + diagonal(row_index, 1, 0)
        # add aligned columns in groups of two
        for col_index in range(parity, cols - 1, 2):
            ascii_line += inside(row_index, col_index, lines_to_top_base) + diagonal(row_index, col_index, 1) + inside(row_index - (not parity), col_index + 1, lines_to_bottom_base) + diagonal(row_index, col_index + 2, 0)
        # add an upper hexagon half that advances by one column to align with the lower hexagon halves
        if not parity:
            ascii_line += inside(row_index, cols - 1, line_index) + diagonal(row_index, cols - 1, 1)
        ascii_line += '\n'
            
        return ascii_line


    def inside(row_index: int, col_index: int, line_index: int) -> str:
        """ Return inside line of hexagon in ASCII. 
            lines_below_base is lines below top of this hexagon.
        TODO:
            Tidy this function up a bit and add comments - this function will be restructured when fill() is implemented
        """

        # print(row_index, col_index)
        tile_ascii = fill_system(row_index, col_index)
        tile_lines = tile_ascii.split('\n')
        # print(tile_lines)
        # print(line_index)
        return tile_lines[line_index - 1]


        lines_to_nearest_base = min(line_index, 2 * Y_SCALE - line_index)

        if line_index == Y_SCALE:
            position = get_position((row_index, col_index))
            if position:
                # tile_id = map_grid[*position]['id'].ljust(3)        Python 3.11
                tile_id = map_grid[row_index, col_index]['id'].ljust(3)
            else:
                tile_id = 3 * ' '
            return tile_id + (X_SCALE + 2 * (lines_to_nearest_base) - 3) * ' '
            
        return (X_SCALE + 2 * (lines_to_nearest_base)) * ' '


    def buffer(line_index: int) -> str:
        """ Return line buffer to align hexagon bases in ASCII. """
        lines_to_nearest_base = min(line_index, 2 * Y_SCALE - line_index)
        return (Y_SCALE - lines_to_nearest_base) * ' '

    @cache
    def share_count(neighbours: tuple[tuple[int, int], ...]) -> int:
        """ Return number of hexagons that share edges/vertices. """
        count = 0
        for position in neighbours:
            count += bool(get_position(position))
        return count

    @cache
    def get_position(position, default=None) -> TileID:
        x, y = position
        if not 0 <= x < rows or not 0 <= y < cols:
            return None
        # value = map_grid[*position]['id']     Python 3.11
        value = map_grid[x, y]['id']
        if value in ['-1', '0']:
            return default
        return value

    @cache
    def fill_system(row_index: int, col_index: int) -> str:
        position = get_position((row_index, col_index))
        if not position:
            return NO_TILE
        tile_info = map_grid[row_index, col_index]
        tile_id = tile_info['id']
        if tile_id in ['-1', '0']:
            return NO_TILE
        
        tile_planets = tile_info['planets']
        tile_ascii = TILE_TEMPLATES[X_SCALE, Y_SCALE][len(tile_planets)]

        tile_ascii = tile_ascii.replace('id0', tile_id.ljust(3))

        for planet_index, planet in enumerate(tile_planets):
            id = str(planet_index)
            # legendary status
            legendary = ' ◐' if planet['legendary'] else '  '
            tile_ascii = tile_ascii.replace('l' + id, legendary)
            # technology specialty
            specialty = {'biotic': 'G', 'cybernetic': 'Y', 'propulsion': 'B', 'warfare': 'R', None: ''}[planet['specialty']].rjust(2)
            tile_ascii = tile_ascii.replace('s' + id, specialty)
            # resources
            resources = str(planet['resources']).rjust(2)
            tile_ascii = tile_ascii.replace('r' + id, resources)
            # influence
            influence = str(planet['influence']).rjust(2)
            tile_ascii = tile_ascii.replace('i' + id, influence)
            # name and trait
            # trait = f"({planet['trait'][0].upper()})"
            trait = {'industrial': '(I)', 'hazardous': '(H)', 'cultural': '(C)', None: ''}[planet['trait']]
            name = planet['name'] + ' ' + trait
            name_lines = textwrap.TextWrapper(width=10).wrap(text=name)
            name_lines.append("")                                                           # in case no wrapping occurs
            tile_ascii = tile_ascii.replace('n' + id + 'a', name_lines[0].ljust(10))
            tile_ascii = tile_ascii.replace('n' + id + 'b', name_lines[1].ljust(10))

        print(tile_ascii)
        return tile_ascii

    
    SCALE = 3   # 2
    X_SCALE = [3, 6, 14, 15, 18, 21][SCALE]
    Y_SCALE = [2, 3,  6,  7,  8,  9][SCALE]
    # X_SCALE, Y_SCALE = 14, 6

    rows, cols = map_grid.shape

    map_ascii = ""
    for row_index in range(rows + 1):                           # account for lower final row in odd indexed columns
        map_ascii += bases(row_index, 0)                        # 0 parity bases
        for line_index in range(1, Y_SCALE):
            map_ascii += insides(row_index, line_index)         # 0 parity insides
        map_ascii += bases(row_index, Y_SCALE)                  # 1 parity bases
        for line_index in range(Y_SCALE + 1, 2 * Y_SCALE):
            map_ascii += insides(row_index, line_index)         # 1 parity insides

    # !!! remember to pseudo-strip ascii_map


    # print(fill_system(2, 1))
    
    return map_ascii

    

tile_grid = spiral_to_tile_grid(MAP_LIST)
print(tile_grid)
map_grid = tile_grid_to_map_grid(tile_grid)
print(map_grid)
ascii_str = map_grid_to_ascii(map_grid)
print(ascii_str)
