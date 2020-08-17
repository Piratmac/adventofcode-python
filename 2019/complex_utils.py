"""
Small library for complex numbers
"""
from math import sqrt, atan2


class ReturnTypeWrapper(type):
    def __new__(mcs, name, bases, dct):
        cls = type.__new__(mcs, name, bases, dct)
        for attr, obj in cls.wrapped_base.__dict__.items():
            # skip 'member descriptor's and overridden methods
            if type(obj) == type(complex.real) or attr in dct:
                continue
            if getattr(obj, "__objclass__", None) is cls.wrapped_base:
                setattr(cls, attr, cls.return_wrapper(obj))
        return cls

    def return_wrapper(cls, obj):
        def convert(value):
            return cls(value) if type(value) is cls.wrapped_base else value

        def wrapper(*args, **kwargs):
            return convert(obj(*args, **kwargs))

        wrapper.__name__ = obj.__name__
        return wrapper


class SuperComplex(complex):
    __metaclass__ = ReturnTypeWrapper
    wrapped_base = complex

    def __lt__(self, other):
        return abs(other - self) < 0

    def __le__(self, other):
        return abs(other - self) <= 0

    def __gt__(self, other):
        return abs(other - self) > 0

    def __ge__(self, other):
        return abs(other - self) >= 0

    def __str__(self):
        return "(" + str(self.real) + "," + str(self.imag) + ")"

    def __add__(self, no):
        return SuperComplex(self.real + no.real, self.imag + no.imag)

    def __sub__(self, no):
        return SuperComplex(self.real - no.real, self.imag - no.imag)

    def phase(self):
        return atan2(self.imag, self.real)

    def amplitude(self):
        return sqrt(self.imag ** 2 + self.real ** 2)


j = SuperComplex(1j)

# Cardinal directions
north = j
south = -j
west = -1
east = 1
northeast = 1 + j
northwest = -1 + j
southeast = 1 - j
southwest = -1 - j

directions_straight = [north, south, west, east]
directions_diagonals = directions_straight + [
    northeast,
    northwest,
    southeast,
    southwest,
]

# To be multiplied by the current cartinal direction
relative_directions = {
    "left": j,
    "right": -j,
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
    elif mode == "manhattan":
        complexes.sort(key=lambda a: manhattan_distance(0, a))
    else:
        complexes.sort(key=lambda a: sqrt(a.imag ** 2 + a.real ** 2))
    return complexes
