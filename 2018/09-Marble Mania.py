# -------------------------------- Input data -------------------------------- #
import os, collections

test_data = {}

test = 1
test_data[test]   = {"input": """9 players; last marble is worth 25 points""",
                     "expected": ['32', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """10 players; last marble is worth 1618 points""",
                     "expected": ['8317', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """13 players; last marble is worth 7999 points""",
                     "expected": ['146373', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """17 players; last marble is worth 1104 points""",
                     "expected": ['2764', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """21 players; last marble is worth 6111 points""",
                     "expected": ['54718', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """30 players; last marble is worth 5807 points""",
                     "expected": ['37305', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": '404 players; last marble is worth 71852 points',
                     "expected": ['434674', '3653994575'],
                    }

# -------------------------------- Control program execution -------------------------------- #

case_to_test = 'real'
part_to_test = 2

# -------------------------------- Initialize some variables -------------------------------- #

puzzle_input           = test_data[case_to_test]['input']
puzzle_expected_result = test_data[case_to_test]['expected'][part_to_test-1]
puzzle_actual_result   = 'Unknown'


# -------------------------------- Actual code execution -------------------------------- #

for string in puzzle_input.split('\n'):
    nb_players, _, _, _, _, _, points, _ = string.split(' ')
    nb_players, points = map(int, (nb_players, points))


if part_to_test == 2:
    points *= 100

position = 0
scores = [0] * nb_players
if part_to_test == 1:
    marbles = [0, 1]
    for new_marble in range(2, points + 1):
        if new_marble % 23 == 0:
            scores[new_marble % nb_players] += new_marble
            position = (position-7) % len(marbles)
            scores[new_marble % nb_players] += marbles[position-1]
            del marbles[position-1]
        else:
            marbles.insert(position+1, new_marble)
            position = ((position + 2) % len(marbles))

        if new_marble % 10000 == 0:
            print (new_marble)


else:
    marbles = collections.deque([0, 1])
    for new_marble in range(2, points + 1):
        if new_marble % 23 == 0:
            scores[new_marble % nb_players] += new_marble
            marbles.rotate(7)
            scores[new_marble % nb_players] += marbles.pop()
            marbles.rotate(-1)
        else:
            marbles.rotate(-1)
            marbles.append(new_marble)

puzzle_actual_result = max(scores)




# -------------------------------- Outputs / results -------------------------------- #

print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




