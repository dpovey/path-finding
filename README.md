# Programming Challeng
The following contains a solution to the programming challenge:
[https://docs.google.com/document/d/1O8OpciNPNJ0MAWyUWAu55W1irLTNSd_9Vs974Wcg0hc/edit?usp=sharing
]()

The program is written in python, it consists of the following files:

* `util.py`: utility functions to dump maps
* `gen-map.py`: program to generate random maps with obstacles
* `shortest-path.py`: program to find the shortest path for a given map


## gen-map.py

```

usage: gen-map.py [-h] [--density DENSITY] [-c] [-s] rows cols

Generate maps

positional arguments:
  rows               number of rows
  cols               number of columns

optional arguments:
  -h, --help         show this help message and exit
  --density DENSITY  density of random obstacles to generate
  -c, --colorize     colorize output
  -s, --space        add additional horizontal space
```

## shortest-path.py

```
usage: shortest-path.py [-h] [-c] [-s] [--original] [--allow-diagonals]

Shortest path for map read from stdin

optional arguments:
  -h, --help         show this help message and exit
  -c, --colorize     colorize output
  -s, --space        add additional horizontal space
  --original         also dump original map
  --allow-diagonals  allow diagonal moves if adjacent cells are blocked
```

## Sample input
`python gen-map.py 10 10 --density=.4 > map`

```
XXXXXXXXXX
X   X    X
X  XX    X
X XXO  X X
X     X XX
XXX X    X
X XXX  XSX
X     XX X
XX X    XX
XXXXXXXXXX
```

## Sample output

`python shortest-path.py < map`

```
XXXXXXXXXX
X   X    X
X  XX    X
X XX`  X X
X    ^X XX
XXX X<<<^X
X XXX  XSX
X     XX X
XX X    XX
XXXXXXXXXX
Cost: 6.414213562373095
```

**Notes**
Both programs take a `--colorize` option that will dump the maps with ANSI terminal colors. This makes it a little easy to debug.

The shortest path program supports an option `--allow-diagonals` the defines the treatment of diagonal moves where the destination
cell is collision-free, but both horizontal and vertical adjacent cells are not.
