# -------------------------------- Input data ---------------------------------------- #
import os, grid, graph, dot, assembly, re, itertools
from collections import Counter, deque, defaultdict

from compass import *
from copy import deepcopy


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
    "input": """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12""",
    "expected": ["71", "Unknown"],
}


test = 2
test_data[test] = {
    "input": """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9""",
    "expected": ["Unknown", "row, class, seat ==> 0"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["32835", "514662805187"],
}


# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #
validations = {}

section = 0
tickets = []

for string in puzzle_input.split("\n"):
    if string == "":
        section += 1
    else:
        if section == 0:
            field, numbers = string.split(": ")
            numbers = positive_ints(numbers)
            validations[field] = list(range(numbers[0], numbers[1] + 1)) + list(
                range(numbers[2], numbers[3] + 1)
            )
        elif section == 1:
            if string == "your ticket:":
                pass
            else:
                my_ticket = ints(string)
        elif section == 2:
            if string == "nearby tickets:":
                pass
            else:
                tickets.append(ints(string))

if part_to_test == 1:
    invalid_fields = 0
    for ticket in tickets:
        invalid_fields += sum(
            [
                field
                for field in ticket
                if all(field not in val for val in validations.values())
            ]
        )

    puzzle_actual_result = invalid_fields

else:
    valid_tickets = []
    invalid_fields = 0
    for ticket in tickets:
        if (
            len(
                [
                    field
                    for field in ticket
                    if all(field not in val for val in validations.values())
                ]
            )
            == 0
        ):
            valid_tickets.append(ticket)

    field_order = {}
    for field in validations.keys():
        possible_order = list(range(len(validations)))
        allowed_values = validations[field]
        for position in range(len(validations)):
            for ticket in valid_tickets:
                # #print (field, ticket, position, possible_order, allowed_values)
                value = ticket[position]
                if value not in allowed_values:
                    try:
                        possible_order.remove(position)
                    except ValueError:
                        pass
        field_order[field] = possible_order

    # #for val in field_order:
    # #print(field_order[val], val)
    while any(len(val) > 1 for val in field_order.values()):
        new_field_order = deepcopy(field_order)
        for field in field_order:
            if len(field_order[field]) == 1:
                for field2 in new_field_order:
                    if field2 == field:
                        pass
                    else:
                        new_field_order[field2] = [
                            val
                            for val in new_field_order[field2]
                            if val not in field_order[field]
                        ]
        field_order = deepcopy(new_field_order)

    ticket_value = 1
    # #for val in field_order:
    # #print(field_order[val], val)
    for field in validations.keys():
        if field[:9] == "departure":
            # #print(
            # #my_ticket, field, field_order[field], my_ticket[field_order[field][0]]
            # #)
            ticket_value *= my_ticket[field_order[field][0]]

    puzzle_actual_result = ticket_value


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2020-12-16 06:05:34.085933
# Part 1: 2020-12-16 06:23:05
# Part 2: 2020-12-16 06:59:59
