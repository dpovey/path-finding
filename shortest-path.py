import sys
import math
import argparse
from util import dump
from copy import deepcopy

def parse_map():
    map = [list(line.rstrip()) for line in list(sys.stdin)]

    start = None
    goal = None

    # Make sure we have same number of columns in each row
    rows = len(map)
    assert(rows >= 3)
    cols = len(map[0])
    assert(cols >= 3)
    for row in map:
        if (len(row) != cols):
            raise Exception('All rows must have the same number of columns')

    # Find start and goal
    for row in range(0, len(map)):
        for col in range(0, len(map[row])):
            val = map[row][col]
            if (val == 'S'):
                start = (row, col)
            elif (val == 'O'):
                goal = (row, col)

    if (start == None):
        raise Exception('Cannot find start')

    if (goal == None):
        raise Exception('Cannot find goal')

    return (map, start, goal)

def is_diagonal_move(y0, x0, y1, x1):
    return y0 != y1 and x0 != x1

def is_illegal_diagonal(map, y, x, i, j):
    if (args.allow_diagonals):
        # All diagnoals that are collision free are legal
        return False

    # Make sure it's a diagonal move        
    if (not is_diagonal_move(y, x, i, j)):
        return False

    # Make sure adjacent cells are collision free as well
    return map[y][j] == 'X' and map[i][x] == 'X'
                   
def succ(map, q):
    succ = []
    (y, x) = q
    rows = len(map)
    cols = len(map[0])

    # depending on the global setting of args.allow_diagonals we may not only have to handle collisions at the final square
    # but also collisions on the diagonal move
    #
    # So:
    #
    #    01
    #  0 #S
    #  1 O#
    #
    # The move from S (0, 1) -> O (1, 0) via the diagonal is not allowed if both 0, 0 and 0, 1
    # are occupied
    for i in range(max(0, y-1), min(y+2, rows)):
        for j in range(max(0, x-1), min(cols, x+2)):
            if ((i, j) != q and map[i][j] != 'X'):
                # Handle diagonal moves
                if (not is_illegal_diagonal(map, y, x, i, j)):
                    succ.append((i, j))
    return succ

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.append(current)
    total_path.reverse()
    return total_path

# NB: This must underestimate or be equal to the actual cost, for this reason, we use straight line
# distance. This is simpler although it would also be acceptable to rasterize the straight line to get a
# more accurate upper bound
def heuristic_cost(start, goal):
    return distance(start, goal, adjacent_only=False)

def distance(start, goal, adjacent_only=True):
    (y0, x0) = start
    (y1, x1) = goal
    dy = y1 - y0
    dx = x1 - x0
    if adjacent_only:
        assert (dx <= 1)
        assert (dy <= 1)
    return math.sqrt(dx * dx + dy * dy)

def min_f(open_set, f_score):
    # Naive way to do this, f_score should be a prioritised queue
    return min(open_set, key=f_score.get)

def a_star(map, start, goal):
    # The set of nodes already evaluated
    closed_set = set()

    # The set of currently discovered nodes that are not evaluated yet.
    # Initially, only the start node is known.
    open_set = set()
    open_set.add(start)

    # For each node, which node it can most efficiently be reached from.
    # If a node can be reached from many nodes, cameFrom will eventually contain the
    # most efficient previous step.
    came_from = {}

    # For each node, the cost of getting from the start node to that node. Default is infinity
    g_score = {}

    # For each node, the total cost of getting from the start node to the goal
    # by passing by that node. That value is partly known, partly heuristic.
    f_score = {}

    # Initialize g and f scores to infinity
    for i in range(0, len(map)):
        for j in range(0, len(map[0])):
            g_score[(i, j)] = math.inf
            f_score[(i, j)] = math.inf

    # The cost of going from start to start is zero.
    g_score[start] = 0    

    # For the first node, that value is completely heuristic.
    f_score[start] = heuristic_cost(start, goal)
    
    while len(open_set) > 0:
        current = min_f(open_set, f_score)
        del f_score[current]

        if current == goal:
            return reconstruct_path(came_from, current)

        open_set.remove(current)
        closed_set.add(current)

        for neighbor in succ(map, current):
            if neighbor in closed_set:
                # Ignore the neighbor which is already evaluated.
                continue 

            # The distance from start to a neighbor
            tentative_gscore = g_score[current] + distance(current, neighbor)

            if not neighbor in open_set:
                # Discover a new node
                open_set.add(neighbor)
            elif tentative_gscore >= g_score[neighbor]:
                continue

            # Note best path so far
            came_from[neighbor] = current
            g_score[neighbor] = tentative_gscore
            f_score[neighbor] = g_score[neighbor] + heuristic_cost(neighbor, goal)

def path_cost(start, path):
    last = start
    cost = 0
    for current in path:
        cost = cost + distance(last, current)
        last = current
    return cost

def write_move(map, last, current):
    MOVES = [[ '`', '^', '/'], [ '<', 'S', '>'], [ ',', 'V', '\\']]
    (y0, x0) = last
    (y1, x1) = current
    dy = y1 - y0
    dx = x1 - x0
    map[y1][x1] = MOVES[dy + 1][dx + 1]

def write_path(map, start, path):
    new_map = deepcopy(map)
    last = start
    for current in path:
        write_move(new_map, last, current)
        last = current
    return new_map

def main():
    # Read map from stdin
    (map, start, goal) = parse_map()

    # Dump original map if requested
    if (args.original):
        dump(map, args)

    # Find shortest path
    path = a_star(map, start, goal)
    if path:
        new_map = write_path(map, start, path)
        dump(new_map, args)
        print('Cost:', path_cost(start, path))
    else:
        print('Not reachable.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Shortest path for map read from stdin')
    parser.add_argument('-c', '--colorize', dest='colorize', action='store_true', help='colorize output')
    parser.add_argument('-s', '--space', dest='space', action='store_true', help='add additional horizontal space')
    parser.add_argument('--original', dest='original', action='store_true', help='also dump original map')
    parser.add_argument('--allow-diagonals', dest='allow_diagonals', action='store_true', help='allow diagonal moves if adjacent cells are blocked')
    args = parser.parse_args()
    main()
