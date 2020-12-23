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

all_ingredients = defaultdict(int)
all_allergens = {}
nb_allergens = defaultdict(int)
allergens_ingredients = {}

for string in puzzle_input.split("\n"):
    if "contains" in string:
        ingredients = string.split(" (")[0].split(" ")
        allergens = string.split("(contains ")[1][:-1].split(", ")
        if isinstance(allergens, str):
            allergens = [allergens]

        for allergen in allergens:
            nb_allergens[allergen] += 1
            if allergen not in all_allergens:
                all_allergens[allergen] = ingredients.copy()
                allergens_ingredients[allergen] = defaultdict(int)
                allergens_ingredients[allergen].update(
                    {ingredient: 1 for ingredient in ingredients}
                )

            else:
                for ingredient in ingredients:
                    allergens_ingredients[allergen][ingredient] += 1
                for ingredient in all_allergens[allergen].copy():
                    if ingredient not in ingredients:
                        all_allergens[allergen].remove(ingredient)

        for ingredient in ingredients:
            all_ingredients[ingredient] += 1

    else:
        print("does not contain any allergen")


for allergen in test:
    if allergen != "shellfish":
        continue
    print(
        allergen,
        test2[allergen],
        [ing for ing, val in test[allergen].items() if val == test2[allergen]],
    )

sum_ingredients = 0
for ingredient in all_ingredients:
    if not (any(ingredient in val for val in all_allergens.values())):
        sum_ingredients += all_ingredients[ingredient]

if part_to_test == 1:
    puzzle_actual_result = sum_ingredients


else:
    allergens_ingredients = {
        aller: [
            ing
            for ing, val in allergens_ingredients[aller].items()
            if val == nb_allergens[aller]
        ]
        for aller in nb_allergens
    }
    final_allergen = {}
    while len(final_allergen) != len(nb_allergens):
        for allergen, val in allergens_ingredients.items():
            if len(val) == 1:
                final_allergen[allergen] = val[0]

        allergens_ingredients = {
            aller: [
                ing
                for ing in allergens_ingredients[aller]
                if ing not in final_allergen.values()
            ]
            for aller in nb_allergens
        }

    print(final_allergen)
    ing_list = ""
    for aller in sorted(final_allergen.keys()):
        ing_list += final_allergen[aller] + ","
    puzzle_actual_result = ing_list[:-1]

# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2020-12-21 06:07:34.505688
# Part 1: 2020-12-21 07:22:36
# Part 2: 2020-12-21 07:30:15
