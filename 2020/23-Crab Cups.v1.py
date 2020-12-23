# -------------------------------- Input data ---------------------------------------- #
import os, grid, graph, dot, assembly, re, itertools
from collections import Counter, deque, defaultdict

from compass import *
from doubly_linked_list import *


# This functions come from https://github.com/mcpower/adventofcode - Thanks!
def lmap(func, *iterables):
    return list(map(func, *iterables))


def ints(s: str):
    return lmap(int, re.findall(r"-?\d+", s))  # thanks mserrano!


def positive_ints(s: str):
    return lmap(int, re.findall(r"\d+", s))  # thanks mserrano!


def floats(s: str):
    return lmap(float, re.findall(r"-?\d+(?:\.\d+)?", s))


def positive_floats(s: str):
    return lmap(float, re.findall(r"\d+(?:\.\d+)?", s))


def words(s: str):
    return re.findall(r"[a-zA-Z]+", s)


test_data = {}

test = 1
test_data[test] = {
    "input": """389125467""",
    "expected": ["92658374 after 10 moves, 67384529 after 100 moves", "149245887792"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["45286397", "836763710"],
}


# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #


if part_to_test == 1:
    moves = 100
    for string in puzzle_input.split("\n"):
        cups = [int(x) for x in string]

    for i in range(moves):
        cur_cup = cups[0]
        pickup = cups[1:4]
        del cups[0:4]

        try:
            dest_cup = max([x for x in cups if x < cur_cup])
        except:
            dest_cup = max([x for x in cups])
        cups[cups.index(dest_cup) + 1 : cups.index(dest_cup) + 1] = pickup
        cups.append(cur_cup)

        print(cups)

    pos1 = cups.index(1)
    puzzle_actual_result = "".join(map(str, cups[pos1 + 1 :] + cups[:pos1]))

else:
    moves = 10 ** 7
    nb_cups = 10 ** 6
    cups = DoublyLinkedList(True)

    for string in puzzle_input.split("\n"):
        for cup in string:
            cups.append(cup)

    new_cups = {
        str(i): DoublyLinkedListElement(str(i), None, None)
        for i in range(10, nb_cups + 1)
    }
    for key, cup in new_cups.items():
        if key != "10":
            cup.prev_element = new_cups[str(int(key) - 1)]
        if key != str(nb_cups):
            cup.next_element = new_cups[str(int(key) + 1)]
    new_cups["10"].prev_element = cups.elements[string[-1]]
    new_cups[str(nb_cups)].next_element = cups.elements[string[0]]

    cups.elements.update(new_cups)
    cups.elements[string[-1]].next_element = new_cups["10"]
    cups.elements[string[0]].prev_element = new_cups[str(nb_cups)]

    del new_cups

    print([(i, cups.elements[str(i)]) for i in map(str, range(1, 15))])

    cur_cup = cups.start_element
    # #print (cups.elements)
    for i in range(1, moves + 1):
        print("----- Move", i)
        # #print (','.join([x.item for x in cups.traverse(cups.start_element)]), cur_cup.item)

        cups_moved = [
            cur_cup.next_element,
            cur_cup.next_element.next_element,
            cur_cup.next_element.next_element.next_element,
        ]
        cups_moved_int = list(map(lambda i: int(i.item), cups_moved))
        # #print ('Moved cups', [x.item for x in cups_moved])

        cups.delete_by_value(cur_cup.next_element)
        cups.delete_by_value(cur_cup.next_element)
        cups.delete_by_value(cur_cup.next_element)

        dest_cup_nr = int(cur_cup.item) - 1
        while dest_cup_nr in cups_moved_int or dest_cup_nr <= 0:
            dest_cup_nr -= 1
            if dest_cup_nr <= 0:
                dest_cup_nr = nb_cups
        dest_cup = cups.find(str(dest_cup_nr))

        # #print ("Destination", dest_cup_nr)

        cups.insert(dest_cup, cups_moved)
        cur_cup = cur_cup.next_element

    pos1 = cups.find("1")
    puzzle_actual_result = int(pos1.next_element.item) * int(
        pos1.next_element.next_element.item
    )
    # #puzzle_actual_result = cups[(pos1+1)%len(cups)] * cups[(pos1+2)%len(cups)]

# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2020-12-23 06:25:17.546310
