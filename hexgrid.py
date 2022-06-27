from functools import cache
import numpy as np
from math import ceil, sqrt
from components.systems_and_planets import SYSTEMS

MAP_STRING = "1"
# MAP_STRING = "1 2 3 4 5 6 7"
# MAP_STRING = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19"
# MAP_STRING = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37"
# MAP_STRING = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61"
# or you can use https://keeganw.github.io/ti4
# MAP_STRING = "18 30 26 40 79 38 71 68 48 76 80 69 47 62 25 34 43 37 28 0 61 73 0 50 21 0 45 77 0 29 42 0 23 49 0 20 60"
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

def spiral_to_grid(map_spiral) -> np.array:
    """ Convert TTS string (tiles in a clockwise hexagonal spiral) to a grid for printing. """
    RING_MAX = spiral_length_to_rings(len(map_spiral))
    array_size = 2 * RING_MAX + 1
    # map_grid = -np.ones((array_size, array_size))
    map_grid = np.full((array_size, array_size), "-1", dtype=object)

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
        # print(map_grid)
        map_grid[x][y] = tile_id

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
    # print(map_grid)
    return map_grid


def grid_to_ascii(map_grid) -> str:
    """
    Still working on this function set to make it more readable
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
    """

    # ---------- components ---------- #
    def bases(row_num, line_index):

        def bases_on(row_index):
            """
            Parameters:
                row_index: row_index for hexagon below the base
            """
            lines_to_nearest_base = 0
            ascii_line = ""
            # print cols in groups of 2s
            ascii_line += buffer(lines_to_nearest_base) + corner(row_index, 0, 0)
            for col_index in range(0, cols - 1, 2):
                ascii_line += base(row_index, col_index) + corner(row_index, col_index, 1) + inside(Y_SCALE, row_index - 1, col_index + 1) + corner(row_index, col_index + 2, 0)
            if cols % 2:
                ascii_line += base(row_index, cols - 1) + corner(row_index, cols - 1, 1)
            ascii_line += '\n'
                
            return ascii_line

        def bases_off(row_index):
            """
            Parameters:
                row_index: row_index for hexagon below the base
            """
            lines_to_nearest_base = Y_SCALE
            ascii_line = ""
            ascii_line += buffer(lines_to_nearest_base) + corner(row_index, -1, 1)
            # print cols in groups of 2s
            for col_index in range(1, cols, 2):
                ascii_line += inside(Y_SCALE, row_index, col_index - 1) + corner(row_index, col_index, 0) + base(row_index, col_index) + corner(row_index, col_index, 1)
            if cols % 2:
                ascii_line += inside(Y_SCALE, row_index, cols - 1) + corner(row_index, cols, 0)
            ascii_line += '\n'
                
            return ascii_line

        def corner(row_index, col_index, corner_index) -> str:
            """ Return corner of hexagon in ASCII.
            
            Parameters:
                row_index: row_index for hexagon below corner
                col_index: col_index for hexagon below corner
                corner_index: 0 for left, 1 for right
            """
            # get neighbour positions, clockwise from (row_index, col_index)

            # unoptimised version: better demonstrates how vector is calculated.
            # code golf attempt:
            # neighbours = ((row_index, col_index),
            #               (row_index - 1, col_index),
            #               (row_index, col_index + 1))
            
            # optimised version: only calculate what we need
            # incorrect now. Update to match unoptimised version
            if not col_index % 2:   # even
                if not corner_index:    # 0
                    neighbours = ((row_index, col_index),
                                (row_index - 1, col_index - 1),
                                (row_index - 1, col_index))
                                
                else:                   # 1
                    neighbours = ((row_index, col_index),
                                (row_index - 1, col_index),
                                (row_index - 1, col_index + 1))
                    
            else:                   # odd
                if not corner_index:    # 0
                    neighbours = ((row_index, col_index),
                                (row_index, col_index - 1),
                                (row_index - 1, col_index))
                                
                else:                   # 1
                    neighbours = ((row_index, col_index),
                                (row_index - 1, col_index),
                                (row_index, col_index + 1))

            # return characters
            count = share_count(neighbours)
            is_below = share_count(((row_index, col_index),))
            is_above = share_count(((row_index - 1, col_index),))

            if not count:
                return ' '
            elif count == 1 and (is_below ^ is_above):
                if is_below:
                    return '.'
                else:               # is_above
                    return '\''
            else:
                if corner_index:    # 1
                    return '{'
                else:               # 0
                    return '}'

        def base(row_index, col_index) -> str:
            """ Return base of hexagon in ASCII.

            Parameters:
                row_index: row_index for hexagon below the base
                col_index: col_index for hexagon
            """
            # get neighbour positions, clockwise from (row_index, col_index)
            neighbours = ((row_index, col_index),
                        (row_index - 1, col_index))

            # return characters
            count = share_count(neighbours)
            if not count:
                return X_SCALE * ' '
            return X_SCALE * '—'    # em-dash


        if line_index == 0:
            return bases_on(row_num)
        else:
            return bases_off(row_num)


    def insides(row_num, line_index):
        def insides_on(row_index, line_index):
            """ I think the lines_to_---_base are misnamed. Must check. """
            lines_to_top_base = Y_SCALE - line_index
            lines_to_bottom_base = line_index        

            ascii_line = ""
            ascii_line += buffer(lines_to_bottom_base) + diagonal(row_index, 0, 0)
            # print cols in groups of 2s
            for col_index in range(0, cols - 1, 2):
                ascii_line += inside(lines_to_bottom_base) + diagonal(row_index, col_index, 1) + inside(lines_to_top_base) + diagonal(row_index, col_index + 2, 0)
            if cols % 2:
                ascii_line += inside(lines_to_bottom_base) + diagonal(row_index, cols - 1, 1)
            ascii_line += '\n'
                
            return ascii_line

        def insides_off(row_index, line_index):
            """ I think the lines_to_---_base are misnamed. Must check. """
            lines_to_bottom_base = 2 * Y_SCALE - line_index
            lines_to_top_base = line_index - Y_SCALE

            ascii_line = ""
            ascii_line += buffer(lines_to_bottom_base) + diagonal(row_index, -1, 1)
            # print cols in groups of 2s
            for col_index in range(1, cols, 2):
                ascii_line += inside(lines_to_bottom_base) + diagonal(row_index, col_index, 0) + inside(lines_to_top_base) + diagonal(row_index, col_index, 1)
            if cols % 2:
                ascii_line += inside(lines_to_bottom_base) + diagonal(row_index, cols, 0)
            ascii_line += '\n'
                
            return ascii_line

        def diagonal(row_index, col_index, diagonal_index) -> str:
            """ Return diagonal of hexagon in ASCII.
            
            Parameters:
                row_index: row_index for hexagon below diagonal
                col_index: col_index for hexagon below diagonal
                diagonal_index: 0 for left, 1 for right
            """
            # get neighbour positions, clockwise from (row_index, col_index)
            if not col_index % 2:   # even
                if not diagonal_index:  # 0
                    neighbours = ((row_index, col_index),
                                (row_index - 1, col_index - 1))
                                
                else:                   # 1
                    neighbours = ((row_index, col_index),
                                (row_index - 1, col_index + 1))
                    
            else:                   # odd
                if not diagonal_index:  # 0
                    neighbours = ((row_index, col_index),
                                (row_index, col_index - 1))
                                
                else:                   # 1
                    neighbours = ((row_index, col_index),
                                (row_index, col_index + 1))
            
            # code golf attempt:
            # neighbours = ((row_index, col_index),
            #               (row_index, col_index + 1))

            # return characters
            count = share_count(neighbours)
            if not count:
                return ' '
            else:
                if diagonal_index:    # 1
                    return '\\'
                else:               # 0
                    return '/'

        if line_index < Y_SCALE:
            return insides_on(row_num, line_index)
        else:
            return insides_off(row_num, line_index)

    def inside(line_index: int, row_index: int = -1, col_index: int = -1) -> str:
        """ Return inside line of hexagon in ASCII. 
            lines_below_base is lines below top of this hexagon. """

        def fill(line_index: int, row_index: int, col_index: int) -> str:
            pass

        # lines_to_nearest_base = min(lines_from_top_base, Y_SCALE - )
        lines_to_nearest_base = line_index     # !!!
        if lines_to_nearest_base == Y_SCALE:
            position = get_position((row_index, col_index))
            if position:
                tile_id = map_grid[row_index][col_index].ljust(3)
                print(tile_id)
            else:
                tile_id = 3 * ' '
            return tile_id + (X_SCALE + 2 * (lines_to_nearest_base) - 3) * ' '
        return (X_SCALE + 2 * (lines_to_nearest_base)) * ' '


    def buffer(lines_to_nearest_base: int) -> str:
        """ Return line buffer to align hexagon bases in ASCII. """
        return (Y_SCALE - lines_to_nearest_base) * ' '

    @cache
    def share_count(neighbours: tuple[tuple[int, int], ...]) -> int:
        """ Return number of hexagons that share edges/vertices. """
        # return sum(map(get_position, neighbours))
        # print(len(neighbours), neighbours, end=': ')

        count = 0
        for position in neighbours:
            if get_position(position):
                count += 1
                # print(position, end=' ')
        # print(count)
        return count

    @cache
    def get_position(position):
        x, y = position
        if not 0 <= x < rows or not 0 <= y < cols:
            return None
        value = map_grid[x][y]
        if value in ["-1", "0"]:
            return None
        return value

    
    SCALE = 3   # 2
    X_SCALE = [3, 6, 14, 15, 18, 21][SCALE]
    Y_SCALE = [2, 3,  6,  7,  8,  9][SCALE]
    # X_SCALE, Y_SCALE = 14, 6

    rows, cols = map_grid.shape

    map_ascii = ""
    for row_num in range(rows + 1):                         # account for final row in off-columns being lower
        map_ascii += bases(row_num, 0)                      # on-column bases
        for line_index in range(1, Y_SCALE):
            map_ascii += insides(row_num, line_index)      # insides
        map_ascii += bases(row_num, Y_SCALE)                     # off-column bases
        for line_index in range(Y_SCALE + 1, 2 * Y_SCALE):
            map_ascii += insides(row_num, line_index)     # insides

    # !!! remember to pseudo-strip ascii_map

    return map_ascii

    

map_grid = spiral_to_grid(MAP_LIST)
print(map_grid)
print(grid_to_ascii(map_grid))




