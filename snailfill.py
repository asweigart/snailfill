"""
Snailfill - A demonstration of the flood fill algorithm in Python using snails and yarn balls as a metaphor.
"""

import random, copy, sys
from typing import List, Tuple

try:
    import bext
except:
    print('You need to install the bext module to run this program.')
    print('From a Terminal (macOS and Linux) or Command Prompt (Windows),')
    print('run `pip3 install bext` and run this program again.')
    sys.exit()


# Constants for objects on the grid:
SNAIL = '@'
#YARN = '0'

UNSLIMED = '.'
SLIMED = 'S'
BLOCKED = 'X'

# Set up the constants for line characters:
UP_DOWN_CHAR         = chr(9474)  # Character 9474 is '│'
LEFT_RIGHT_CHAR      = chr(9472)  # Character 9472 is '─'
DOWN_RIGHT_CHAR      = chr(9484)  # Character 9484 is '┌'
DOWN_LEFT_CHAR       = chr(9488)  # Character 9488 is '┐'
UP_RIGHT_CHAR        = chr(9492)  # Character 9492 is '└'
UP_LEFT_CHAR         = chr(9496)  # Character 9496 is '┘'

def displayGrid(grid, snailx, snaily, yarnTrail):
    #print('DEBUG snailx, snaily =', snailx, snaily)
    #print('DEBUG yanrTrail =', yarnTrail)

    # Add the yarn to the grid:
    grid = copy.copy(grid)
    yarnTrail = copy.copy(yarnTrail)
    yarnTrail.append((snailx, snaily))

    if len(yarnTrail) == 0:
        pass  # Do nothing.
    if len(yarnTrail) == 1:
        grid[yarnTrail[0]] = '/' # Yarn by itself in one location will just look like a slash.
    elif len(yarnTrail) >= 2:
        # For yarn of length 2, just use the left-right or up-down character:
        if yarnTrail[0][0] == yarnTrail[1][0]:
            grid[yarnTrail[0]] = UP_DOWN_CHAR
        elif yarnTrail[0][1] == yarnTrail[1][1]:
            grid[yarnTrail[0]] = LEFT_RIGHT_CHAR

        if len(yarnTrail) >= 3:
            # Draw the appropriate box-drawing character line based on the previous and next location of the line.
            for i in range(1, len(yarnTrail) - 1):
                prevx, prevy = yarnTrail[i - 1]
                yarnx, yarny = yarnTrail[i]
                nextx, nexty = yarnTrail[i + 1]
                # Figure out which line character to place at yarnx, yarny in grid:
                if (prevx, prevy) == (yarnx - 1, yarny):
                    # Yarn is coming from the left.
                    if (nextx, nexty) == (yarnx + 1, yarny):
                        # Yarn is going to the right.
                        grid[(yarnx, yarny)] = LEFT_RIGHT_CHAR
                    elif (nextx, nexty) == (yarnx, yarny - 1):
                        # Yarn is going up.
                        grid[(yarnx, yarny)] = UP_LEFT_CHAR
                    elif (nextx, nexty) == (yarnx, yarny + 1):
                        # Yarn is going down.
                        grid[(yarnx, yarny)] = DOWN_LEFT_CHAR
                elif (prevx, prevy) == (yarnx + 1, yarny):
                    # Yarn is coming from the right.
                    if (nextx, nexty) == (yarnx - 1, yarny):
                        # Yarn is going to the left.
                        grid[(yarnx, yarny)] = LEFT_RIGHT_CHAR
                    elif (nextx, nexty) == (yarnx, yarny - 1):
                        # Yarn is going up.
                        grid[(yarnx, yarny)] = UP_RIGHT_CHAR
                    elif (nextx, nexty) == (yarnx, yarny + 1):
                        # Yarn is going down.
                        grid[(yarnx, yarny)] = DOWN_RIGHT_CHAR
                elif (prevx, prevy) == (yarnx, yarny - 1):
                    # Yarn is coming from above.
                    if (nextx, nexty) == (yarnx + 1, yarny):
                        # Yarn is going to the right.
                        grid[(yarnx, yarny)] = UP_RIGHT_CHAR
                    elif (nextx, nexty) == (yarnx - 1, yarny):
                        # Yarn is going to the left.
                        grid[(yarnx, yarny)] = UP_LEFT_CHAR
                    elif (nextx, nexty) == (yarnx, yarny + 1):
                        # Yarn is going down.
                        grid[(yarnx, yarny)] = UP_DOWN_CHAR
                elif (prevx, prevy) == (yarnx, yarny + 1):
                    # Yarn is coming from below.
                    if (nextx, nexty) == (yarnx + 1, yarny):
                        # Yarn is going to the right.
                        grid[(yarnx, yarny)] = DOWN_RIGHT_CHAR
                    elif (nextx, nexty) == (yarnx - 1, yarny):
                        # Yarn is going to the left.
                        grid[(yarnx, yarny)] = DOWN_LEFT_CHAR
                    elif (nextx, nexty) == (yarnx, yarny - 1):
                        # Yarn is going up.
                        grid[(yarnx, yarny)] = UP_DOWN_CHAR


    for y in range(HEIGHT):
        for x in range(WIDTH):
            if x == snailx and y == snaily:
                bext.fg('green')
                print(SNAIL, end='')
            elif grid[(x, y)] in (UNSLIMED, BLOCKED):
                bext.fg('white')
                print(grid[(x, y)], end='')
            else:
                bext.fg('green')
                if grid[(x, y)] == SLIMED:
                    print('.', end='')
                else:
                    print(grid[(x, y)], end='')

        print()
    print()


START_X = 0
START_Y = 0

# Edit the GRID_MAP string as desired. Periods are open spaces, Xs are blocked spaces.
# You can change this map to whatever you want:
GRID_MAP = """
........................................
.................X......................
................X.X.....................
...............X...X....................
..............X....X....................
.....XXXXXX..X.....X....................
....X......XX.......X...................
.....XX..............XXXXXXXXXXX........
.......XX......................X........
.........XXXX.................X.........
.............X..............XX..........
............X............XXX............
...........X............X...............
...........X.............X..............
...........X.....XXXXX....X.............
...........X....X.....XX...X............
...........X...X........X...X...........
............X.X..........X...X..........
.............X............XXXX..........
........................................
"""[1:-1].splitlines()

HEIGHT = len(GRID_MAP)
WIDTH = len(GRID_MAP[0])

# Create the grid:
grid = {}  # Keys are (x, y) tuples, values are strings from the legend.
for x in range(WIDTH):
    for y in range(HEIGHT):
        grid[(x, y)] = GRID_MAP[y][x]

snailx = START_X
snaily = START_Y
yarnTrail = []  # type: List[Tuple[int, int]]
#bext.clear()

while True:
    #displayGrid(grid, snailx, snaily, yarnTrail)
    #bext.fg('white')
    #input('Press Enter to continue...')
    #bext.clear()
    grid[(snailx, snaily)] = SLIMED

    # Get a list of the unvisited (i.e. unslimed) neighboring spaces:
    unvisitedNeighbors = []

    # Check the neighboring space to the left:
    if snailx > 0 and grid[(snailx - 1, snaily)] == UNSLIMED:
        unvisitedNeighbors.append((snailx - 1, snaily, 'left'))
    # Check the neighboring space to the right:
    if snailx < WIDTH - 1 and grid[(snailx + 1, snaily)] == UNSLIMED:
        unvisitedNeighbors.append((snailx + 1, snaily, 'right'))
    # Check the neighboring space above:
    if snaily > 0 and grid[(snailx, snaily - 1)] == UNSLIMED:
        unvisitedNeighbors.append((snailx, snaily - 1, 'up'))
    # Check the neighboring space below:
    if snaily < HEIGHT - 1 and grid[(snailx, snaily + 1)] == UNSLIMED:
        unvisitedNeighbors.append((snailx, snaily + 1, 'down'))


    if len(unvisitedNeighbors) == 0 and len(yarnTrail) == 0:
        # If we have backtracked all the yarn, then we are done:
        break
    elif len(unvisitedNeighbors) == 0:
        # We are backtracking along the trail of yarn:
        snailx, snaily = yarnTrail.pop()
        #print('The snail backtracked along the yarn.')
    else:
        yarnTrail.append((snailx, snaily)) # Unspool more yarn from the yarn ball here.

        # Visit a random neighboring space:
        snailx, snaily, movedTo = random.choice(unvisitedNeighbors)
        #print('The snail moved ' + movedTo + '.')

bext.fg('white')
displayGrid(grid, snailx, snaily, yarnTrail)
