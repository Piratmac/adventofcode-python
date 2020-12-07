# -------------------------------- Input data ---------------------------------------- #
import os, grid, graph, dot, assembly, re, itertools
from collections import Counter, deque, defaultdict

from compass import *


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
    "input": """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.""",
    "expected": ["4", "Unknown"],
}

test = 2
test_data[test] = {
    "input": """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.""",
    "expected": ["Unknown", "126"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["300", "8030"],
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
    results = []
    for string in puzzle_input.split("\n"):
        results.append(re.findall("[a-z ]* bags?", string))

    combinations = []
    for result in results:
        if len(result) == 1:
            print("No match for", result)
        else:
            combinations.append(
                {
                    "out": result[0].replace("bags", "bag"),
                    "in": [x.replace("bags", "bag")[1:] for x in result[1:]],
                }
            )

    contain_gold = set(["shiny gold bag"])
    # There is certainly a clever way to reduce how many loops I do, but I don't know it (yet)
    for i in range(len(combinations)):
        for combination in combinations:
            if any(
                [gold_container in combination["in"] for gold_container in contain_gold]
            ):
                contain_gold.add(combination["out"])
                print(len(contain_gold), i, len(combinations))

    puzzle_actual_result = len(contain_gold) - 1


else:
    results = []
    for string in puzzle_input.split("\n"):
        results.append(re.findall("([0-9]* )?([a-z ]*) bags?", string))

    combinations = []
    for result in results:
        if len(result) == 1:
            bags = result[0][1].split(" bags contain no ")
            combinations.append({"out": bags[0], "in": []})
        else:
            combinations.append(
                {"out": result[0][1], "in": {x[1]: int(x[0]) for x in result[1:]}}
            )

    gold_contains = defaultdict(int)
    gold_contains["shiny gold"] = 1
    gold_contains["total"] = -1

    while len(gold_contains) > 1:
        for combination in combinations:
            if combination["out"] in gold_contains:
                for containee in combination["in"]:
                    # Add those bags to the count
                    gold_contains[containee] += (
                        combination["in"][containee] * gold_contains[combination["out"]]
                    )
                # Add the "out" bag to the count & remove it from the list
                # This ensures we don't loop over the same bag twice
                gold_contains["total"] += gold_contains[combination["out"]]
                del gold_contains[combination["out"]]

        print(sum(gold_contains.values()), gold_contains)

    puzzle_actual_result = gold_contains["total"]


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
