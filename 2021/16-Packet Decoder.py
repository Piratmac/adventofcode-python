# -------------------------------- Input data ---------------------------------------- #
import os, grid, graph, dot, assembly, re, itertools
from collections import Counter, deque, defaultdict
from functools import reduce

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
    "input": """D2FE28""",
    "expected": ["number: 2021", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """38006F45291200""",
    "expected": ["2 subpackets: 10 & 20", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """EE00D40C823060""",
    "expected": ["3 subpackets: 1, 2, 3", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """8A004A801A8002F478""",
    "expected": ["16", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """C200B40A82""",
    "expected": ["Unknown", "3"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["877", "194435634456"],
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


def analyze_packet(binary_value):
    p_version = int(binary_value[0:3], 2)
    p_type = int(binary_value[3:6], 2)
    position = 6

    if p_type == 4:
        group = binary_value[position]
        number = ""
        while binary_value[position] == "1":
            number += binary_value[position + 1 : position + 5]
            position += 5
        number += binary_value[position + 1 : position + 5]
        position += 5

        return {
            "version": p_version,
            "type": p_type,
            "value": int(number, 2),
            "length": position,
        }

    else:
        length_type = int(binary_value[position], 2)
        position += 1
        if length_type == 0:
            length_bits = int(binary_value[position : position + 15], 2)
            position += 15
            subpackets_bits = binary_value[position : position + length_bits]

            subpacket_position = 0
            subpackets = []
            while subpacket_position < len(subpackets_bits):
                subpacket = analyze_packet(subpackets_bits[subpacket_position:])
                subpackets.append(subpacket)
                subpacket_position += subpacket["length"]

        else:
            nb_packets = int(binary_value[position : position + 11], 2)
            position += 11
            subpackets_bits = binary_value[position:]

            subpacket_position = 0
            subpackets = []
            while len(subpackets) != nb_packets:
                subpacket = analyze_packet(subpackets_bits[subpacket_position:])
                subpackets.append(subpacket)
                subpacket_position += subpacket["length"]

        if p_type == 0:
            value = sum([p["value"] for p in subpackets])
        elif p_type == 1:
            value = reduce(lambda x, y: x * y, [p["value"] for p in subpackets])
        elif p_type == 2:
            value = min([p["value"] for p in subpackets])
        elif p_type == 3:
            value = max([p["value"] for p in subpackets])
        elif p_type == 5:
            value = 1 if subpackets[0]["value"] > subpackets[1]["value"] else 0
        elif p_type == 6:
            value = 1 if subpackets[0]["value"] < subpackets[1]["value"] else 0
        elif p_type == 7:
            value = 1 if subpackets[0]["value"] == subpackets[1]["value"] else 0

        return {
            "version": p_version,
            "type": p_type,
            "value": value,
            "length": position + subpacket_position,
            "subpackets": subpackets,
        }


def sum_version(packet):
    total_version = packet["version"]
    if "subpackets" in packet:
        total_version += sum([sum_version(p) for p in packet["subpackets"]])

    return total_version


def operate_packet(packet):
    if "value" in packet:
        return packet["value"]

    else:

        total_version += sum([sum_version(p) for p in packet["subpackets"]])

    return total_version


message = "{0:b}".format(int(puzzle_input, 16))
while len(message) % 4 != 0:
    message = "0" + message


packets = analyze_packet(message)

if part_to_test == 1:
    puzzle_actual_result = sum_version(packets)

else:
    puzzle_actual_result = packets["value"]


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2021-12-16 08:09:42.385082
# Past 1: 2021-12-16 08:43:04
# Past 2: 2021-12-16 09:10:53
