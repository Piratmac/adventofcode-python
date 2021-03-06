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
    "input": """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)""",
    "expected": ["5", "mxmxvkd,sqjhc,fvjkl"],
}

test += 1
test_data[test] = {
    "input": """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)""",
    "expected": ["5", "mxmxvkd,sqjhc,fvjkl"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["2410", "tmp,pdpgm,cdslv,zrvtg,ttkn,mkpmkx,vxzpfp,flnhl"],
}


# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

all_allergens = set()
all_ingredients = {}
allergen_graph = graph.WeightedGraph()
allergen_graph.vertices = set()

for string in puzzle_input.split("\n"):
    if "contains" in string:
        ingredients = string.split(" (")[0].split(" ")
        allergens = string.split("(contains ")[1][:-1].split(", ")

        all_allergens = all_allergens.union(allergens)
        all_ingredients.update(
            {ing: all_ingredients.get(ing, 0) + 1 for ing in ingredients}
        )

        for allergen in allergens:
            if allergen not in allergen_graph.edges:
                allergen_graph.edges[allergen] = {x: 1 for x in ingredients}
            else:
                for ing in allergen_graph.edges[allergen].copy():
                    if ing not in ingredients:
                        del allergen_graph.edges[allergen][ing]

    else:
        print("does not contain any allergen")

allergen_graph.vertices = list(all_allergens.union(set(all_ingredients.keys())))
allergen_graph.bipartite_matching(all_allergens, all_ingredients)

if part_to_test == 1:
    safe_ingredients = [
        x for x in allergen_graph.vertices if allergen_graph.flow_graph[x] == {}
    ]
    safe_number = sum(all_ingredients[x] for x in safe_ingredients)
    puzzle_actual_result = safe_number

else:
    dangerous_ingredients = [
        list(allergen_graph.flow_graph[aller].keys())[0]
        for aller in sorted(all_allergens)
    ]
    puzzle_actual_result = ",".join(dangerous_ingredients)


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2020-12-21 06:07:34.505688
# Part 1: 2020-12-21 07:22:36
# Part 2: 2020-12-21 07:30:15
