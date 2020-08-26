# -------------------------------- Input data ---------------------------------------- #
import os, pathfinding

from complex_utils import *

test_data = {}

test = 1
test_data[test] = {
    "input": (
        """deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1""",
        10,
    ),
    "expected": ["9 2 5 8 1 4 7 0 3 6", "9 2 5 8 1 4 7 0 3 6"],
}

test += 1
test_data[test] = {
    "input": (
        """cut 6
deal with increment 7
deal into new stack""",
        10,
    ),
    "expected": ["3 0 7 4 1 8 5 2 9 6", "3 0 7 4 1 8 5 2 9 6"],
}

test += 1
test_data[test] = {
    "input": (
        """deal with increment 7
cut 3
deal into new stack""",
        10,
    ),
    "expected": ["Unknown", "Unknown"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": (open(input_file, "r+").read(), 119315717514047),
    "expected": ["2480", "62416301438548"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

nb_cards = puzzle_input[1]

if part_to_test == 1:
    deck = [x for x in range(nb_cards)]

    for string in puzzle_input[0].split("\n"):
        if string == "":
            continue
        if string == "deal into new stack":
            deck = deck[::-1]
        elif string[0:4] == "deal":
            number = int(string.split(" ")[-1])
            new_deck = [0] * nb_cards
            for i in range(0, nb_cards * number, number):
                new_deck[i % nb_cards] = deck[i // number]
            deck = new_deck[:]
        else:
            number = int(string.split(" ")[-1])
            deck = deck[number:] + deck[:number]

        # print (string, deck)

    print(deck)
    puzzle_actual_result = deck.index(2019)


else:
    nb_shuffles = 101741582076661
    # Then the goal is to find a, b and x so that after 1 deal means:
    # a*initial_position + b = [output] % nb_cards
    # a and b can be found by analyzing the movements done
    a, b = 1, 0
    for string in puzzle_input[0].split("\n")[::-1]:
        if string == "":
            continue
        if string == "deal into new stack":
            a *= -1
            b *= -1
            b -= 1  # Not sure why it's needed...
        elif string[0:4] == "deal":
            number = int(string.split(" ")[-1])
            a *= pow(number, -1, nb_cards)
            b *= pow(number, -1, nb_cards)
        else:
            number = int(string.split(" ")[-1])
            b += number

        a, b = a % nb_cards, b % nb_cards

    # This function applies the shuffles nb_shuffles times
    # This is the equation a^nb_shuffles * position + sum[a^k * b for k in range(0, nb_shuffles-1)] % nb_cards
    # This translated to a^nb_shuffles * position + b * (1-a^nb_shuffles) / (1-a) % nb_cards

    def shuffles(a, b, position, nb_shuffles, nb_cards):
        value = pow(a, nb_shuffles, nb_cards) * position
        value += b * (1 - pow(a, nb_shuffles, nb_cards)) * pow(1 - a, -1, nb_cards)
        value %= nb_cards
        return value

    puzzle_actual_result = shuffles(a, b, 2020, nb_shuffles, nb_cards)


# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
