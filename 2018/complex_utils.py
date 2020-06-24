"""
Small library for complex numbers
"""
from math import sqrt

# Cardinal directions
north = 1j
south = -1j
west = -1
east = 1
northeast = 1 + 1j
northwest = -1 + 1j
southeast = 1 - 1j
southwest = -1 - 1j

directions_straight = [north, south, west, east]
directions_diagonals = directions_straight + [
    northeast,
    northwest,
    southeast,
    southwest,
]

# To be multiplied by the current cartinal direction
relative_directions = {
    "left": 1j,
    "right": -1j,
    "ahead": 1,
    "back": -1,
}


def min_real(complexes):
    real_values = [x.real for x in complexes]
    return min(real_values)


def min_imag(complexes):
    real_values = [x.imag for x in complexes]
    return min(real_values)


def max_real(complexes):
    real_values = [x.real for x in complexes]
    return max(real_values)


def max_imag(complexes):
    real_values = [x.imag for x in complexes]
    return max(real_values)


def manhattan_distance(a, b):
    return abs(b.imag - a.imag) + abs(b.real - a.real)


def complex_sort(complexes, mode=""):
    # Sorts by real, then by imaginary component (x then y)
    if mode == "xy":
        complexes.sort(key=lambda a: (a.real, a.imag))
    # Sorts by imaginary, then by real component (y then x)
    elif mode == "yx":
        complexes.sort(key=lambda a: (a.imag, a.real))
    # Sorts by negative imaginary, then by real component (-y then x) - 'Reading" order
    elif mode == "reading":
        complexes.sort(key=lambda a: (-a.imag, a.real))
    # Sorts by distance from 0,0 (kind of polar coordinates)
    else:
        complexes.sort(key=lambda a: sqrt(a.imag ** 2 + a.real ** 2))
    return complexes
