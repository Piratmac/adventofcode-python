# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test] = {
    "input": 9,
    "expected": ["5158916779", "Unknown"],
}
test += 1
test_data[test] = {
    "input": 5,
    "expected": ["0124515891", "Unknown"],
}
test += 1
test_data[test] = {
    "input": 18,
    "expected": ["9251071085", "Unknown"],
}
test += 1
test_data[test] = {
    "input": 2018,
    "expected": ["5941429882", "Unknown"],
}

test += 1
test_data[test] = {
    "input": "51589",
    "expected": ["Unknown", "9"],
}
test += 1
test_data[test] = {
    "input": "01245",
    "expected": ["Unknown", "5"],
}
test += 1
test_data[test] = {
    "input": "92510",
    "expected": ["Unknown", "18"],
}
test += 1
test_data[test] = {
    "input": "59414",
    "expected": ["Unknown", "2018"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": "633601",
    "expected": ["5115114101", "20310465"],
}

# -------------------------------- Control program execution -------------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables -------------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution -------------------------------- #

elf1, elf2 = 0, 1
recipes = [3, 7]

if part_to_test == 1:
    while len(recipes) < int(puzzle_input) + 10:
        new_score = recipes[elf1] + recipes[elf2]
        if new_score >= 10:
            recipes.append(new_score // 10)
        recipes.append(new_score % 10)
        elf1 += 1 + recipes[elf1]
        elf2 += 1 + recipes[elf2]
        elf1 %= len(recipes)
        elf2 %= len(recipes)

    puzzle_actual_result = "".join(map(str, recipes[puzzle_input : puzzle_input + 10]))


else:
    recipes = "37"
    puzzle_input = str(puzzle_input)
    while puzzle_input not in recipes[-10:]:
        e1, e2 = int(recipes[elf1]), int(recipes[elf2])
        new_score = e1 + e2
        if new_score >= 10:
            recipes += str(new_score // 10)
        recipes += str(new_score % 10)
        elf1 += 1 + e1
        elf2 += 1 + e2
        elf1 %= len(recipes)
        elf2 %= len(recipes)

    puzzle_actual_result = recipes.find(puzzle_input)


# -------------------------------- Outputs / results -------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
