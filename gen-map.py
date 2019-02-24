# Generates a map to used with the programming challenge
import random
import argparse
from util import dump

def gen_space(cols):
	return [' ' for _ in range(0, cols - 2)] 

def gen_middle_row(cols):
	return ['X'] + gen_space(cols) + ['X']

def set_random(map, val):
	rows = len(map)
	cols = len(map[0])
	x = random.randrange(1, rows - 1)
	y = random.randrange(1, cols - 1)
	map[x][y] = val

def set_random_unless(map, val, no_val):
	rows = len(map)
	cols = len(map[0])
	while True:
		x = random.randrange(1, rows - 1)
		y = random.randrange(1, cols - 1)
		if map[x][y] != no_val:
			map[x][y] = val
			break

def main(rows, cols, obstacle_density):
	assert rows >= 4
	assert cols >= 4
	assert obstacle_density < 1

	# Generate frame
	top = [['X'] * cols]
	middle = [gen_middle_row(cols) for _ in range(1, rows - 1)]
	bottom = [['X'] * cols]
	map = top + middle + bottom

	# Generate obstacles with given density
	n_obstacles = int((rows - 2) * (cols - 2) * obstacle_density)
	for _ in range(0, n_obstacles):
		set_random(map, 'X')

	# Set start
	set_random(map, 'S')

	# Set goal (make sure its not the same as start)
	set_random_unless(map, 'O', 'S')
	dump(map, args)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Generate maps')
	parser.add_argument('--density', default=0.05, type=float,
		help='density of random obstacles to generate')
	parser.add_argument('-c', '--colorize', dest='colorize', action='store_true', help='colorize output')
	parser.add_argument('-s', '--space', dest='space', action='store_true', help='add additional horizontal space')
	parser.add_argument('rows', metavar='rows', type=int, help='number of rows')
	parser.add_argument('cols', metavar='cols', type=int, help='number of columns')
	args = parser.parse_args()

	main(args.rows, args.cols, args.density)
