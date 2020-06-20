# -------------------------------- Input data -------------------------------- #
import os, pathfinding, re

test_data = {}

test = 1
test_data[test]   = {"input": """/->-\\
|   |  /----\\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   """,
                     "expected": ['7,3', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": r"""/>-<\
|   |
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/""",
                     "expected": ['Unknown', '6,4'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read(),
                     "expected": ['124,130', '143, 123'],
                    }

# -------------------------------- Control program execution -------------------------------- #

case_to_test = 'real'
part_to_test = 2
verbose = 3

# -------------------------------- Initialize some variables -------------------------------- #

puzzle_input           = test_data[case_to_test]['input']
puzzle_expected_result = test_data[case_to_test]['expected'][part_to_test-1]
puzzle_actual_result   = 'Unknown'


# -------------------------------- Actual code execution -------------------------------- #

cart_to_track = {'^': '|', '>': '-', '<': '-', 'v': '|'}
up, right, left, down = ((0, -1), (1, 0), (-1, 0), (0, 1))
directions = {'^': up, '>': right, '<': left, 'v': down}
new_dirs = {
    '^':['<', '^', '>'],
    '>':['^', '>', 'v'],
    '<':['v', '<', '^'],
    'v':['>', 'v', '<'],
    '/': {'^': '>', '>': '^', '<': 'v', 'v': '<'},
    '\\':{'^': '<', '>': 'v', '<': '^', 'v': '>'},
}


def move_cart (track, cart):
    (x, y), dir, choice = cart

    x += directions[dir][0]
    y += directions[dir][1]

    if track[y][x] == '+':
        dir = new_dirs[dir][choice]
        choice += 1
        choice %= 3
    elif track[y][x] in ('\\', '/'):
        dir = new_dirs[track[y][x]][dir]

    return ((x, y), dir, choice)

# Setting up the track
track = []
cart_positions = []
carts = []
for y, line in enumerate(puzzle_input.split('\n')):
    track.append([])
    for x, letter in enumerate(line):
        if letter in cart_to_track:
            track[y].append(cart_to_track[letter])
            carts.append(((x, y), letter, 0))
            cart_positions.append((x, y))
        else:
            track[y].append(letter)

# Run them!
tick = 0

carts.append('new')
while len(carts) > 0:
    cart = carts.pop(0)
    if cart == 'new':
        if len(carts) == 1:
            break
        tick += 1
#        print ('tick', tick, 'completed - Remaining', len(carts))
        carts = sorted(carts, key=lambda x: (x[0][1], x[0][0]))
        cart_positions = [c[0] for c in carts]
        cart = carts.pop(0)
        carts.append('new')
    cart_positions.pop(0)



    cart = move_cart(track, cart)

    # Check collisions
    if cart[0] in cart_positions:
        if part_to_test == 1:
            puzzle_actual_result = cart[0]
            break
        else:
            print ('collision', cart[0])
            carts = [c for c in carts if c[0] != cart[0]]
            cart_positions = [c[0] for c in carts]
    else:
        carts.append(cart)
        cart_positions.append(cart[0])

if part_to_test == 2:
    puzzle_actual_result = carts[0][0]



# -------------------------------- Outputs / results -------------------------------- #

print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




