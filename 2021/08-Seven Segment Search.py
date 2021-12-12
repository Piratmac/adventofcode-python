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
    "input": """acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf""",
    "expected": ["Unknown", "5353"],
}

test = 2
test_data[test] = {
    "input": """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce""",
    "expected": [
        "26",
        "8394, 9781, 1197, 9361, 4873, 8418, 4548, 1625, 8717, 4315 ==> 61229",
    ],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["543", "994266"],
}


# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

# Conver integer to 36-character binary
#  str_value = "{0:>036b}".format(value)
# Convert binary string to number
#  value = int(str_value, 2)


if part_to_test == 1:
    nb_digits = 0
    for string in puzzle_input.split("\n"):
        output = words(string)[-4:]
        nb_digits += len([x for x in output if len(x) in [2, 3, 4, 7]])

    puzzle_actual_result = nb_digits


else:
    digit_to_real_segments = {
        "0": "abcefg",
        "1": "cf",
        "2": "acdeg",
        "3": "acdfg",
        "4": "bcdf",
        "5": "abdfg",
        "6": "abdefg",
        "7": "acf",
        "8": "abcdefg",
        "9": "abcdfg",
    }
    digit_container = {
        "0": ["8"],
        "1": ["0", "3", "4", "7", "8", "9"],
        "2": ["8"],
        "3": ["8", "9"],
        "4": ["8", "9"],
        "5": ["6", "8", "9"],
        "6": ["8"],
        "7": ["0", "3", "8", "9"],
        "8": [],
        "9": ["8"],
    }
    shared_segments = {
        digit1: {
            digit2: len(
                [
                    segment
                    for segment in digit_to_real_segments[digit2]
                    if segment in digit_to_real_segments[digit1]
                ]
            )
            for digit2 in digit_to_real_segments
        }
        for digit1 in digit_to_real_segments
    }
    nb_segments = {
        digit: len(digit_to_real_segments[digit]) for digit in digit_to_real_segments
    }
    for digit in digit_to_real_segments:
        digit_to_real_segments[digit] = [
            "r_" + x for x in digit_to_real_segments[digit]
        ]
        digit_to_real_segments[digit].sort()

    digits = [str(i) for i in range(10)]

    sum_displays = 0

    for string in puzzle_input.split("\n"):
        signals = ["".join(sorted(x)) for x in words(string.replace("| ", ""))[:-4]]
        displayed_words = ["".join(sorted(x)) for x in words(string)[-4:]]

        edges = {}
        vertices = signals + digits
        for word in signals:
            edges[word] = [
                digit for digit in nb_segments if nb_segments[digit] == len(word)
            ]

        mapping = {}
        i = 0
        while len(mapping) != 9 and i != 5:
            i += 1
            changed = True
            while changed:
                changed = False
                for word in edges:
                    if len(edges[word]) == 1:
                        mapping[word] = edges[word][0]
                        edges = {
                            w: [edge for edge in edges[w] if edge != mapping[word]]
                            for w in edges
                        }
                        changed = True
                        del edges[word]

            for known_word in mapping:  # abd
                digit = mapping[known_word][0]  # 7

                for word in edges:  # bcdef
                    same_letters = len([x for x in word if x in known_word])
                    for possible_digit in edges[word]:  # '2', '3', '5'
                        if shared_segments[digit][possible_digit] != same_letters:
                            edges[word].remove(possible_digit)

            # exit()

            # Second try, not the right approach (easier to do with shared_segments)

            # for known_word in mapping: # abd
            # digit = mapping[known_word][0] # 7
            # #print ('known_word', known_word, '- digit', digit, 'container', digit_container[digit])
            # if digit_container[digit] == []:
            # continue
            # for word in edges: # bcdef
            # #print ('tried word', word, '- digits', edges[word])
            # for possible_digit in edges[word]: # '2', '3', '5'
            # #print ('possible_digit', possible_digit, possible_digit in digit_container[digit])
            # if possible_digit in digit_container[digit]: # '0', '3', '8', '9'
            # #print ([(letter, letter in word) for letter in known_word])
            # if not all([letter in word for letter in known_word]):
            # edges[word].remove(possible_digit)

        # print (edges, mapping)
        output = ""
        for displayed_word in displayed_words:
            output += "".join(mapping[displayed_word])

        sum_displays += int(output)

    puzzle_actual_result = sum_displays

# First try, too complex

# for string in puzzle_input.split("\n"):
# randomized_words = words(string.replace('| ', ''))
# randomized_displayed_words = words(string)[-4:]

# randomized_segments = [x for x in 'abcdefg']
# real_segments = ['r_'+x for x in 'abcdefg']
# edges = {randomized: {real:1 for real in real_segments} for randomized in randomized_segments}
# vertices = randomized_segments + real_segments

# for randomized_word in randomized_words:
# for randomized_segment in randomized_word:
# possible_segments = []
# for digit in nb_segments:
# if nb_segments[digit] == len(randomized_word):
# possible_segments += digit_to_real_segments[digit]
# possible_segments = set(possible_segments)


# for real_segment in real_segments:
# if real_segment in possible_segments:
# continue
# if randomized_segment in edges:
# if real_segment in edges[randomized_segment]:
# del edges[randomized_segment][real_segment]

# #if randomized_segment in 'be':
# #print (randomized_word, digit, nb_segments[digit], randomized_segment, possible_segments, edges[randomized_segment])
# print (randomized_words)
# print ([x for x in randomized_words if len(x) in [2,3,4,7]])
# print ({x: list(edges[x].keys()) for x in edges})

# mapping = graph.WeightedGraph(vertices, edges)
# result = mapping.bipartite_matching(randomized_segments, real_segments)
# print ('flow_graph ', mapping.flow_graph)
# segment_mapping = {}
# for randomized_segment in mapping.flow_graph:
# segment_mapping[randomized_segment] = mapping.flow_graph[randomized_segment]

# final_number = ''
# for randomized_word in randomized_displayed_words:
# print('')
# real_segments = []
# for letter in randomized_word:
# real_segments.append(''.join([k for k in mapping.flow_graph[letter]]))
# print ('real_segments', real_segments)
# real_segments = list(set(real_segments))
# real_segments.sort()
# real_segments = ''.join(real_segments)


# final_number += ''.join([str(key) for key in digit_to_real_segments if ''.join(digit_to_real_segments[key]) == real_segments])
# print ('real_segments', real_segments)
# print (randomized_word, [(str(key), ''.join(digit_to_real_segments[key])) for key in digit_to_real_segments])
# print (randomized_word, final_number)

# print (final_number)


# break


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2021-12-08 08:11:57.138188
# Part 1 : 2021-12-08 08:13:56
# Part 2 : 2021-12-08 14:12:15
